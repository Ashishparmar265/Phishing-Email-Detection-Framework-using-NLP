const analyzeBtn = document.getElementById('analyzeBtn');
const emailInput = document.getElementById('emailInput');
const results = document.getElementById('results');
const loader = document.getElementById('loader');

analyzeBtn.addEventListener('click', async () => {
    const text = emailInput.value.trim();
    if (!text) return;

    loader.style.display = 'block';
    analyzeBtn.disabled = true;

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        if (!response.ok) throw new Error('API server error');
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        alert('Connection to Analysis Engine failed.');
    } finally {
        loader.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

window.addEventListener('load', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const externalData = urlParams.get('ext_data');
    
    if (externalData) {
        try {
            const decodedData = JSON.parse(externalData);
            if (decodedData && decodedData.body) {
                let formattedText = `Subject: ${decodedData.subject || 'No Subject'}\n`;
                formattedText += `From: ${decodedData.sender || 'Unknown Sender'}\n`;
                formattedText += `-------------------\n\n`;
                formattedText += decodedData.body;
                emailInput.value = formattedText;
                setTimeout(() => analyzeBtn.click(), 500);
            }
        } catch (e) {
            console.error("Extension data parse failed");
        }
    }
});

function displayResults(data) {
    results.style.display = 'block';
    
    const predText = document.getElementById('predictionText');
    const tag = document.getElementById('threatTag');
    
    // Clean display
    predText.textContent = data.prediction.split(' ')[0].toUpperCase();
    tag.textContent = data.threat_level.toUpperCase() + '_RISK';
    
    if (data.threat_level === 'High') {
        predText.style.color = 'var(--danger)';
        tag.style.color = 'var(--danger)';
    } else if (data.threat_level === 'Low') {
        predText.style.color = 'var(--success)';
        tag.style.color = 'var(--success)';
    } else {
        predText.style.color = '#F59E0B';
        tag.style.color = '#F59E0B';
    }

    document.getElementById('probValue').textContent = (data.phishing_probability * 100).toFixed(2) + '%';
    document.getElementById('lstmValue').textContent = data.model_scores.advanced_lstm ? (data.model_scores.advanced_lstm * 100).toFixed(2) + '%' : 'INACTIVE';
    document.getElementById('rfValue').textContent = (data.model_scores.baseline_rf * 100).toFixed(2) + '%';
    
    document.getElementById('urlValue').textContent = data.extracted_features.url_count;
    document.getElementById('urgencyValue').textContent = data.extracted_features.urgency_score.toFixed(3);
    
    results.scrollIntoView({ behavior: 'smooth' });
}
