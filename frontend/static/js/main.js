// Main JavaScript for ResumeSense

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzeForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const resultsSection = document.getElementById('results');
    const errorDiv = document.getElementById('error');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset UI
        resultsSection.style.display = 'none';
        errorDiv.style.display = 'none';
        
        // Show loading state
        analyzeBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        btnLoader.style.display = 'inline-block';

        try {
            const formData = new FormData(form);
            
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }

            // Display results
            displayResults(data);
            resultsSection.style.display = 'block';
            
        } catch (error) {
            console.error('Error:', error);
            errorDiv.textContent = error.message || 'An error occurred during analysis. Please try again.';
            errorDiv.style.display = 'block';
        } finally {
            // Reset button state
            analyzeBtn.disabled = false;
            btnText.textContent = 'Analyze Resume';
            btnLoader.style.display = 'none';
        }
    });

    function displayResults(data) {
        // Quality Score
        const qualityScore = data.quality_score || 0;
        document.getElementById('qualityScore').textContent = qualityScore.toFixed(1);
        const qualityFill = document.getElementById('qualityFill');
        qualityFill.style.width = qualityScore + '%';
        qualityFill.style.background = getScoreColor(qualityScore);

        // ATS Score
        if (data.ats_score !== undefined) {
            document.getElementById('atsCard').style.display = 'block';
            document.getElementById('atsScore').textContent = data.ats_score.toFixed(1);
            const atsFill = document.getElementById('atsFill');
            atsFill.style.width = data.ats_score + '%';
            atsFill.style.background = getScoreColor(data.ats_score);
            
            // ATS Report
            displayATSReport(data.ats_report);
        }

        // Match Score
        if (data.match_score !== null && data.match_score !== undefined) {
            document.getElementById('matchCard').style.display = 'block';
            document.getElementById('matchScore').textContent = data.match_score.toFixed(1) + '%';
            const matchFill = document.getElementById('matchFill');
            matchFill.style.width = data.match_score + '%';
            matchFill.style.background = getScoreColor(data.match_score);
            
            // Match Details
            displayMatchDetails(data.match_details);
        }

        // Power Verbs
        if (data.power_verbs) {
            displayPowerVerbs(data.power_verbs);
        }
    }

    function displayATSReport(atsReport) {
        const atsPanel = document.getElementById('atsPanel');
        const issuesDiv = document.getElementById('atsIssues');
        const recommendationsDiv = document.getElementById('atsRecommendations');

        atsPanel.style.display = 'block';

        // Display issues
        if (atsReport.issues && atsReport.issues.length > 0) {
            issuesDiv.innerHTML = '<h4>Issues Found:</h4>';
            atsReport.issues.forEach(issue => {
                const issueItem = document.createElement('div');
                issueItem.className = 'issue-item';
                issueItem.textContent = issue;
                issuesDiv.appendChild(issueItem);
            });
        } else {
            issuesDiv.innerHTML = '<p style="color: #28a745; font-weight: 600;">✓ No major issues found!</p>';
        }

        // Display recommendations
        if (atsReport.recommendations && atsReport.recommendations.length > 0) {
            recommendationsDiv.innerHTML = '<h4>Recommendations:</h4>';
            atsReport.recommendations.forEach(rec => {
                const recItem = document.createElement('div');
                recItem.className = 'recommendation-item';
                recItem.textContent = rec;
                recommendationsDiv.appendChild(recItem);
            });
        }
    }

    function displayPowerVerbs(verbsData) {
        const verbsPanel = document.getElementById('verbsPanel');
        const verbFindingsDiv = document.getElementById('verbFindings');

        verbsPanel.style.display = 'block';

        if (verbsData.findings && verbsData.findings.length > 0) {
            verbFindingsDiv.innerHTML = '';
            
            verbsData.findings.forEach(finding => {
                const findingDiv = document.createElement('div');
                findingDiv.className = 'verb-finding';
                
                findingDiv.innerHTML = `
                    <strong>Found: "${finding.weak_verb}"</strong>
                    <p style="color: #6c757d; margin: 8px 0; font-size: 0.9em;">${finding.context}</p>
                    <div class="verb-suggestions">
                        <span style="color: #6c757d; margin-right: 8px;">Suggestions:</span>
                        ${finding.suggestions.map(verb => 
                            `<span class="verb-suggestion">${verb}</span>`
                        ).join('')}
                    </div>
                `;
                
                verbFindingsDiv.appendChild(findingDiv);
            });
        } else {
            verbFindingsDiv.innerHTML = '<p style="color: #28a745; font-weight: 600;">✓ No weak verbs found! Your resume uses strong action verbs.</p>';
        }

        // Display stats if available
        if (verbsData.stats) {
            const statsDiv = document.createElement('div');
            statsDiv.style.marginTop = '20px';
            statsDiv.style.padding = '15px';
            statsDiv.style.background = 'white';
            statsDiv.style.borderRadius = '8px';
            statsDiv.innerHTML = `
                <h4>Power Verb Statistics</h4>
                <p>Strong Verbs: ${verbsData.stats.strong_verb_count} | 
                   Weak Verbs: ${verbsData.stats.weak_verb_count} | 
                   Power Verb Score: ${verbsData.stats.power_verb_score.toFixed(1)}%</p>
            `;
            verbFindingsDiv.appendChild(statsDiv);
        }
    }

    function displayMatchDetails(matchDetails) {
        if (!matchDetails) return;

        const matchPanel = document.getElementById('matchPanel');
        const matchDetailsDiv = document.getElementById('matchDetails');

        matchPanel.style.display = 'block';

        let html = '';

        // Common keywords
        if (matchDetails.common_keywords && matchDetails.common_keywords.length > 0) {
            html += '<h4>Matched Keywords:</h4>';
            html += '<div class="match-keywords">';
            matchDetails.common_keywords.forEach(keyword => {
                html += `<span class="keyword matched">${keyword}</span>`;
            });
            html += '</div>';
        }

        // Missing keywords
        if (matchDetails.missing_keywords && matchDetails.missing_keywords.length > 0) {
            html += '<h4 style="margin-top: 20px;">Missing Keywords:</h4>';
            html += '<div class="match-keywords">';
            matchDetails.missing_keywords.forEach(keyword => {
                html += `<span class="keyword missing">${keyword}</span>`;
            });
            html += '</div>';
        }

        // Important keywords
        if (matchDetails.matched_important_keywords && matchDetails.matched_important_keywords.length > 0) {
            html += '<h4 style="margin-top: 20px;">Matched Important Keywords:</h4>';
            html += '<div class="match-keywords">';
            matchDetails.matched_important_keywords.forEach(keyword => {
                html += `<span class="keyword matched">${keyword}</span>`;
            });
            html += '</div>';
        }

        // Stats
        html += '<div style="margin-top: 20px; padding: 15px; background: white; border-radius: 8px;">';
        html += `<p><strong>Important Keywords Matched:</strong> ${matchDetails.important_keywords_matched} / ${matchDetails.important_keywords_total}</p>`;
        html += '</div>';

        matchDetailsDiv.innerHTML = html;
    }

    function getScoreColor(score) {
        if (score >= 80) {
            return 'linear-gradient(90deg, #28a745 0%, #20c997 100%)';
        } else if (score >= 60) {
            return 'linear-gradient(90deg, #ffc107 0%, #ff9800 100%)';
        } else {
            return 'linear-gradient(90deg, #dc3545 0%, #c82333 100%)';
        }
    }
});


