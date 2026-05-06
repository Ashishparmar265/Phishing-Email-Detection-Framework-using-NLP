// popup.js

document.addEventListener('DOMContentLoaded', () => {
    const subjectEl = document.getElementById('subject');
    const senderEl = document.getElementById('sender');
    const bodyEl = document.getElementById('body');
    const urlsEl = document.getElementById('urls');
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const previewArea = document.getElementById('content-preview');
    const notGmailEl = document.getElementById('not-gmail');

    let extractedData = null;

    console.log("PhishGuard Popup: Initializing...");

    // 1. Validate environment
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTab = tabs[0];
        
        if (!activeTab || !activeTab.url.includes("mail.google.com")) {
            console.warn("PhishGuard: Not on Gmail.");
            previewArea.classList.add('hidden');
            analyzeBtn.parentElement.classList.add('hidden');
            notGmailEl.classList.remove('hidden');
            return;
        }

        // 2. Trigger Extraction
        console.log("PhishGuard: Sending extractData message to content script...");
        chrome.tabs.sendMessage(activeTab.id, { action: "extractData" }, (response) => {
            if (chrome.runtime.lastError) {
                console.error("PhishGuard: Error communicating with content script:", chrome.runtime.lastError);
                subjectEl.innerText = "Error: Please refresh Gmail.";
                return;
            }

            if (response) {
                console.log("PhishGuard: Received data from content script:", response);
                extractedData = response;
                
                // Update UI
                subjectEl.innerText = response.subject;
                senderEl.innerText = response.sender;
                
                // Show a decent preview
                const previewText = response.body.length > 500 ? 
                                   response.body.substring(0, 500) + "..." : 
                                   response.body;
                bodyEl.innerText = previewText || "(No body content detected)";
                
                // Enable button if we have data
                if (response.body.length > 10) {
                    analyzeBtn.disabled = false;
                    analyzeBtn.style.opacity = "1";
                } else {
                    console.warn("PhishGuard: Extracted body is too short.");
                    bodyEl.innerText = "Warning: Content too short for accurate analysis.";
                }
            } else {
                console.error("PhishGuard: Received empty response from content script.");
                subjectEl.innerText = "Extraction failed.";
            }
        });
    });

    // 3. Analyze Flow
    analyzeBtn.addEventListener('click', () => {
        if (!extractedData) {
            console.error("PhishGuard: No data to analyze.");
            return;
        }

        console.log("PhishGuard: Preparing data for frontend...");
        
        // Use a safer truncation limit. 
        // Most browsers/servers handle up to 32KB URLs reliably.
        // We limit body to 15k to stay well within limits including subject/sender.
        let bodyToPass = extractedData.body;
        if (bodyToPass.length > 15000) {
            console.warn("PhishGuard: Body too large for URL, truncating to 15k chars.");
            bodyToPass = bodyToPass.substring(0, 15000) + "... [Truncated for Transfer]";
        }

        const dataToTransfer = {
            ...extractedData,
            body: bodyToPass
        };

        try {
            const dataStr = encodeURIComponent(JSON.stringify(dataToTransfer));
            // Try both localhost and 127.0.0.1 in case of mapping issues
            const targetUrl = `http://localhost:8000/ui/index.html?ext_data=${dataStr}`;
            
            console.log("PhishGuard: Data String Length:", dataStr.length);
            console.log("PhishGuard: Opening analysis page...");
            
            chrome.tabs.create({ url: targetUrl });
        } catch (e) {
            console.error("PhishGuard: Failed to encode data:", e);
            alert("Error preparing data for analysis. The email might be too large.");
        }
    });

    clearBtn.addEventListener('click', () => {
        location.reload(); // Simple way to clear
    });
});
