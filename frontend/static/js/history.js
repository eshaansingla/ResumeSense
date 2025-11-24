// History page JavaScript

document.addEventListener('DOMContentLoaded', async function () {
    const historyList = document.getElementById('historyList');

    try {
        const response = await fetch('/api/history?limit=50');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to load history');
        }

        if (data.length === 0) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📄</div>
                    <h3>No Analysis History</h3>
                    <p>You haven't analyzed any resumes yet.</p>
                    <a href="/" class="btn-primary" style="margin-top: 20px; text-decoration: none; display: inline-block;">Analyze Your First Resume</a>
                </div>
            `;
            return;
        }

        historyList.innerHTML = '';

        data.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';

            const date = new Date(item.created_at);
            const formattedDate = date.toLocaleString();

            let scoresHtml = '';
            if (item.quality_score !== null) {
                scoresHtml += `
                    <div class="history-score">
                        <span class="history-score-label">Quality</span>
                        <span class="history-score-value">${item.quality_score.toFixed(1)}</span>
                    </div>
                `;
            }
            if (item.ats_score !== null) {
                scoresHtml += `
                    <div class="history-score">
                        <span class="history-score-label">ATS</span>
                        <span class="history-score-value">${item.ats_score.toFixed(1)}</span>
                    </div>
                `;
            }
            if (item.match_score !== null) {
                scoresHtml += `
                    <div class="history-score">
                        <span class="history-score-label">Match</span>
                        <span class="history-score-value">${item.match_score.toFixed(1)}%</span>
                    </div>
                `;
            }

            historyItem.innerHTML = `
                <div class="history-item-header">
                    <h3>Analysis #${item.id}</h3>
                    <span class="history-item-date">${formattedDate}</span>
                </div>
                <div class="history-scores">
                    ${scoresHtml}
                </div>
                ${item.resume_preview ? `
                    <div class="history-preview">
                        <strong>Resume Preview:</strong><br>
                        ${item.resume_preview}
                    </div>
                ` : ''}
                ${item.jd_preview ? `
                    <div class="history-preview">
                        <strong>Job Description Preview:</strong><br>
                        ${item.jd_preview}
                    </div>
                ` : ''}
            `;

            historyList.appendChild(historyItem);
        });

    } catch (error) {
        console.error('Error loading history:', error);
        historyList.innerHTML = `
            <div class="error-message">
                <strong>Error:</strong> ${error.message}
            </div>
        `;
    }
});


