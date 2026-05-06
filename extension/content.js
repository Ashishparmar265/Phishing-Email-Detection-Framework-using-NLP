// content.js
// Enhanced scraper for Gmail dynamic DOM

console.log("PhishGuard: Content script loaded.");

/**
 * Robustly find the email body in Gmail's complex structure
 */
function getEmailBody() {
    // Priority 1: Standard a3s class (most common)
    // We look for the visible one to handle threaded conversations
    const bodies = document.querySelectorAll('div.a3s.aiL');
    for (const b of bodies) {
        if (b.offsetWidth > 0 || b.offsetHeight > 0) {
            return b;
        }
    }

    // Priority 2: Alternative container for some HTML emails
    const altBodies = document.querySelectorAll('div[role="listitem"] div[dir="ltr"]');
    if (altBodies.length > 0) {
        return altBodies[altBodies.length - 1]; // Usually the latest message
    }

    // Priority 3: Very broad fallback
    return document.querySelector('.ii.gt');
}

/**
 * Extract data with retries for dynamic content
 */
async function extractWithRetry(retries = 3, delay = 1000) {
    for (let i = 0; i < retries; i++) {
        console.log(`PhishGuard: Extraction attempt ${i + 1}...`);
        const data = attemptExtraction();
        
        // If we found a body and a subject, consider it a success
        if (data.body && data.body.length > 50 && data.subject !== "Unknown Subject") {
            console.log("PhishGuard: Extraction successful!");
            return data;
        }
        
        console.log("PhishGuard: Content not fully loaded, retrying...");
        await new Promise(resolve => setTimeout(resolve, delay));
    }
    return attemptExtraction(); // Final attempt
}

function attemptExtraction() {
    // 1. Subject Extraction
    // Gmail uses h2.hP for the thread subject
    let subject = document.querySelector('h2.hP')?.innerText || 
                  document.querySelector('h1[role="heading"]')?.innerText || 
                  "Unknown Subject";

    // 2. Sender Extraction
    // Gmail uses span.gD for the sender name/email
    const senderElement = document.querySelector('span.gD');
    let senderName = senderElement?.innerText || "Unknown Sender";
    let senderEmail = senderElement?.getAttribute('email') || "";
    
    // Fallback for sender if gD fails
    if (!senderEmail) {
        const altSender = document.querySelector('span[email]');
        senderEmail = altSender?.getAttribute('email') || "";
        senderName = altSender?.innerText || senderName;
    }

    const sender = senderEmail ? `${senderName} <${senderEmail}>` : senderName;

    // 3. Body Extraction
    const bodyContainer = getEmailBody();
    let bodyText = bodyContainer?.innerText || "";
    
    // If it's a very short text, check if we're hitting a hidden div
    if (bodyText.length < 20 && bodyContainer) {
        bodyText = bodyContainer.textContent || "";
    }

    // NEW: I-Frame Conversion logic
    // If the email contains an iframe, we extract its source URL and treat it as content
    if (bodyContainer) {
        const iframes = bodyContainer.querySelectorAll('iframe');
        iframes.forEach((frame, index) => {
            const frameSrc = frame.src || frame.getAttribute('src');
            if (frameSrc && !frameSrc.startsWith('javascript:')) {
                bodyText += `\n\n[RESOLVED IFRAME URL #${index + 1}: ${frameSrc}]\n`;
                console.log(`PhishGuard: Converted iframe src to URL content: ${frameSrc}`);
            }
        });
    }

    // 4. URL Extraction (Comprehensive)
    const urls = [];
    if (bodyContainer) {
        // A. Extract from <a> tags and buttons
        const links = bodyContainer.querySelectorAll('a, [role="button"]');
        links.forEach(link => {
            let href = link.href || link.getAttribute('href') || link.getAttribute('data-saferedirecturl');
            const text = link.innerText?.trim() || link.getAttribute('aria-label') || "Link";
            
            if (href && !href.startsWith('mailto:') && !href.startsWith('javascript:')) {
                // CLEAN/UNWRAP URLs: Convert tracking redirects to final URLs
                if (href.includes('redirect=') || href.includes('url=')) {
                    try {
                        const urlMatch = href.match(/(?:redirect|url)=([^&]+)/);
                        if (urlMatch && urlMatch[1]) {
                            const unwrapped = decodeURIComponent(urlMatch[1]);
                            if (unwrapped.startsWith('http')) {
                                href = unwrapped;
                                console.log("PhishGuard: Unwrapped redirect URL:", href);
                            }
                        }
                    } catch(e) {}
                }
                
                urls.push({ text, href });
            }
        });

        // B. Robust Regex for plain text URLs (Handling complex Naukri-style links)
        const urlRegex = /https?:\/\/[^\s<"']+/g;
        const textToSearch = bodyContainer.innerText + " " + bodyContainer.textContent;
        const matches = textToSearch.match(urlRegex);
        
        if (matches) {
            matches.forEach(match => {
                let cleanMatch = match.replace(/[)\].,;]$/, "");
                
                // UNWRAP plain text redirects
                if (cleanMatch.includes('redirect=') || cleanMatch.includes('url=')) {
                    try {
                        const innerMatch = cleanMatch.match(/(?:redirect|url)=([^&]+)/);
                        if (innerMatch && innerMatch[1]) {
                            const unwrapped = decodeURIComponent(innerMatch[1]);
                            if (unwrapped.startsWith('http')) {
                                cleanMatch = unwrapped;
                            }
                        }
                    } catch(e) {}
                }

                if (!urls.find(u => u.href === cleanMatch)) {
                    urls.push({ text: "[Text URL]", href: cleanMatch });
                }
            });
        }
    }

    // Also append the first few found URLs to the body text for the NLP model to see
    if (urls.length > 0) {
        bodyText += "\n\n--- Extracted Links for Analysis ---\n";
        urls.slice(0, 5).forEach(u => {
            bodyText += `${u.href}\n`;
        });
    }

    const result = {
        subject: subject.trim(),
        sender: sender.trim(),
        body: bodyText.trim(),
        urls: urls.slice(0, 20) // Capture more for analysis
    };

    console.log("PhishGuard Extracted Data Snapshot:", {
        subject: result.subject,
        bodyLength: result.body.length,
        urlCount: result.urls.length
    });

    return result;
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractData") {
        extractWithRetry().then(data => {
            sendResponse(data);
        });
        return true; // Keep async channel open
    }
});
