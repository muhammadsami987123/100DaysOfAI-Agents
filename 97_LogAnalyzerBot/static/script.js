// LogAnalyzerBot - Main JavaScript

let currentLogData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // File upload
    const fileInput = document.getElementById('logFile');
    const fileUploadBox = document.getElementById('fileUploadBox');
    
    if (fileUploadBox) {
        fileUploadBox.addEventListener('click', () => fileInput.click());
        fileUploadBox.addEventListener('dragover', handleDragOver);
        fileUploadBox.addEventListener('drop', handleDrop);
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }
    
    // Content upload
    const uploadContentBtn = document.getElementById('uploadContentBtn');
    if (uploadContentBtn) {
        uploadContentBtn.addEventListener('click', handleContentUpload);
    }
    
    // Analyze button
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', handleAnalyze);
    }
    
    // Explain error buttons (delegated)
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('explain-btn')) {
            const errorMessage = e.target.dataset.error;
            explainError(errorMessage);
        }
    });
}

// Check API status
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.loaded) {
            showAlert(`Loaded ${data.total_entries} log entries`, 'success');
        }
        
        if (!data.api_available) {
            showAlert('AI features unavailable: No API key configured', 'info');
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading('uploadStatus', 'Uploading and parsing log file...');
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert(`✅ ${data.message}`, 'success');
            enableAnalysis();
        } else {
            showAlert(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Upload failed: ${error.message}`, 'error');
    } finally {
        hideLoading('uploadStatus');
    }
}

// Handle content upload
async function handleContentUpload() {
    const content = document.getElementById('logContent').value;
    
    if (!content.trim()) {
        showAlert('Please paste some log content', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('content', content);
    
    showLoading('uploadStatus', 'Parsing log content...');
    
    try {
        const response = await fetch('/api/analyze-content', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert(`✅ ${data.message}`, 'success');
            enableAnalysis();
        } else {
            showAlert(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Analysis failed: ${error.message}`, 'error');
    } finally {
        hideLoading('uploadStatus');
    }
}

// Handle analysis
async function handleAnalyze() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const logLevels = Array.from(document.querySelectorAll('input[name="logLevels"]:checked'))
        .map(cb => cb.value).join(',');
    const keyword = document.getElementById('keyword').value;
    const includeAI = document.getElementById('includeAI').checked;
    
    const formData = new FormData();
    if (startDate) formData.append('start_date', startDate);
    if (endDate) formData.append('end_date', endDate);
    if (logLevels) formData.append('log_levels', logLevels);
    if (keyword) formData.append('keyword', keyword);
    formData.append('include_ai', includeAI);
    
    showLoading('analysisStatus', 'Analyzing logs...');
    document.getElementById('resultsSection').classList.add('hidden');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentLogData = data;
            displayResults(data);
            hideLoading('analysisStatus');
        } else {
            showAlert(`❌ Analysis failed: ${data.error}`, 'error');
            hideLoading('analysisStatus');
        }
    } catch (error) {
        showAlert(`❌ Analysis failed: ${error.message}`, 'error');
        hideLoading('analysisStatus');
    }
}

// Display results
function displayResults(data) {
    document.getElementById('resultsSection').classList.remove('hidden');
    
    // Update stats
    document.getElementById('totalEntries').textContent = data.total_entries || 0;
    document.getElementById('totalErrors').textContent = data.total_errors || 0;
    document.getElementById('totalWarnings').textContent = data.total_warnings || 0;
    document.getElementById('totalCritical').textContent = data.total_critical || 0;
    
    // Most frequent error
    if (data.most_frequent_error) {
        const [error, count] = data.most_frequent_error;
        document.getElementById('frequentError').textContent = 
            `${error.substring(0, 100)}... (${count}x)`;
    }
    
    // Affected modules
    if (data.affected_modules && data.affected_modules.length > 0) {
        document.getElementById('affectedModules').textContent = 
            data.affected_modules.slice(0, 5).join(', ');
    }
    
    // Known issues
    displayKnownIssues(data.known_issues || []);
    
    // Timeline
    displayTimeline(data.timeline || []);
    
    // AI insights
    if (data.ai_insights) {
        document.getElementById('aiInsights').textContent = data.ai_insights;
        document.getElementById('aiInsightsCard').classList.remove('hidden');
    }
}

// Display known issues
function displayKnownIssues(issues) {
    const container = document.getElementById('issuesList');
    
    if (issues.length === 0) {
        container.innerHTML = '<p>No known issues detected</p>';
        return;
    }
    
    container.innerHTML = issues.map(issue => `
        <div class="issue-item">
            <div class="issue-header">
                <div class="issue-title">${issue.issue_type}</div>
                <div class="issue-count">${issue.count} occurrences</div>
            </div>
            <div class="issue-suggestion">
                💡 ${issue.suggestion}
            </div>
            ${issue.sample_entries && issue.sample_entries.length > 0 ? `
                <details style="margin-top: 0.5rem;">
                    <summary style="cursor: pointer; color: var(--info-color);">
                        View sample errors
                    </summary>
                    <div style="margin-top: 0.5rem; font-size: 0.85rem; font-family: monospace;">
                        ${issue.sample_entries.map(e => `<div style="margin: 0.5rem 0;">• ${e}</div>`).join('')}
                    </div>
                </details>
            ` : ''}
        </div>
    `).join('');
}

// Display timeline
function displayTimeline(timeline) {
    const container = document.getElementById('timelineList');
    
    if (timeline.length === 0) {
        container.innerHTML = '<p>No timeline events</p>';
        return;
    }
    
    container.innerHTML = timeline.map(event => `
        <div class="timeline-item ${event.level.toLowerCase()}">
            <div class="timeline-timestamp">
                ${event.timestamp !== 'Unknown' ? new Date(event.timestamp).toLocaleString() : 'Unknown time'}
            </div>
            <div class="timeline-source">
                ${event.level} - ${event.source}
            </div>
            <div class="timeline-message">${event.message}</div>
        </div>
    `).join('');
}

// Explain error
async function explainError(errorMessage) {
    const formData = new FormData();
    formData.append('error_message', errorMessage);
    formData.append('log_level', 'ERROR');
    formData.append('source', 'unknown');
    formData.append('frequency', '1');
    
    showLoading('errorExplanation', 'Getting AI explanation...');
    
    try {
        const response = await fetch('/api/explain-error', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('errorExplanation').textContent = data.explanation;
        } else {
            showAlert(`❌ Failed to get explanation: ${data.error}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Explanation failed: ${error.message}`, 'error');
    } finally {
        hideLoading('errorExplanation');
    }
}

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.style.borderColor = 'var(--primary-color)';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.style.borderColor = 'var(--border-color)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const fileInput = document.getElementById('logFile');
        fileInput.files = files;
        handleFileUpload({ target: fileInput });
    }
}

// Enable analysis section
function enableAnalysis() {
    document.getElementById('analysisSection').classList.remove('hidden');
    document.getElementById('analyzeBtn').disabled = false;
}

// Show alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 5000);
}

// Loading state
function showLoading(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="loading"></div> ${message}`;
        element.classList.remove('hidden');
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('hidden');
    }
}

