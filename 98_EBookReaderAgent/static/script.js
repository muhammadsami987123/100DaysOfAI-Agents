// EBookReaderAgent - Main JavaScript

let currentBookInfo = null;
let currentChapters = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkStatus();
});

// Setup event listeners
function setupEventListeners() {
    // Input method toggle
    const toggleFile = document.getElementById('toggleFile');
    const toggleUrl = document.getElementById('toggleUrl');
    const fileInputSection = document.getElementById('fileInputSection');
    const urlInputSection = document.getElementById('urlInputSection');
    
    if (toggleFile && toggleUrl) {
        toggleFile.addEventListener('click', () => switchInputMethod('file'));
        toggleUrl.addEventListener('click', () => switchInputMethod('url'));
    }
    
    // File upload
    const fileInput = document.getElementById('bookFile');
    const fileUploadBox = document.getElementById('fileUploadBox');
    
    if (fileUploadBox) {
        fileUploadBox.addEventListener('click', () => fileInput.click());
        fileUploadBox.addEventListener('dragover', handleDragOver);
        fileUploadBox.addEventListener('drop', handleDrop);
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }
    
    // URL loading
    const loadUrlBtn = document.getElementById('loadUrlBtn');
    const bookUrl = document.getElementById('bookUrl');
    
    if (loadUrlBtn) {
        loadUrlBtn.addEventListener('click', handleUrlLoad);
    }
    
    if (bookUrl) {
        bookUrl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleUrlLoad();
            }
        });
    }
    
    // Action buttons
    const summarizeAllBtn = document.getElementById('summarizeAllBtn');
    if (summarizeAllBtn) {
        summarizeAllBtn.addEventListener('click', handleSummarizeAll);
    }
    
    const getTakeawaysBtn = document.getElementById('getTakeawaysBtn');
    if (getTakeawaysBtn) {
        getTakeawaysBtn.addEventListener('click', handleGetTakeaways);
    }
    
    const getQuotesBtn = document.getElementById('getQuotesBtn');
    if (getQuotesBtn) {
        getQuotesBtn.addEventListener('click', handleGetQuotes);
    }
    
    const analyzeBookBtn = document.getElementById('analyzeBookBtn');
    if (analyzeBookBtn) {
        analyzeBookBtn.addEventListener('click', handleAnalyzeBook);
    }
    
    // Question button
    const askQuestionBtn = document.getElementById('askQuestionBtn');
    if (askQuestionBtn) {
        askQuestionBtn.addEventListener('click', handleAskQuestion);
    }
    
    // Enter key for question input
    const questionInput = document.getElementById('questionInput');
    if (questionInput) {
        questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleAskQuestion();
            }
        });
    }
    
    // Clear results button
    const clearResultsBtn = document.getElementById('clearResultsBtn');
    if (clearResultsBtn) {
        clearResultsBtn.addEventListener('click', () => {
            const resultsSection = document.getElementById('resultsSection');
            resultsSection.classList.add('hidden');
        });
    }
    
    // Chapter click handlers (delegated)
    document.addEventListener('click', (e) => {
        if (e.target.closest('.chapter-item')) {
            const chapterItem = e.target.closest('.chapter-item');
            const chapterNumber = parseInt(chapterItem.dataset.chapterNumber);
            handleSummarizeChapter(chapterNumber);
        }
    });
}

// Switch input method
function switchInputMethod(method) {
    const toggleFile = document.getElementById('toggleFile');
    const toggleUrl = document.getElementById('toggleUrl');
    const fileInputSection = document.getElementById('fileInputSection');
    const urlInputSection = document.getElementById('urlInputSection');
    
    if (method === 'file') {
        toggleFile.classList.add('active');
        toggleUrl.classList.remove('active');
        fileInputSection.classList.remove('hidden');
        urlInputSection.classList.add('hidden');
    } else {
        toggleUrl.classList.add('active');
        toggleFile.classList.remove('active');
        urlInputSection.classList.remove('hidden');
        fileInputSection.classList.add('hidden');
    }
}

// Check API status
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (!data.api_available) {
            showAlert('AI features may be unavailable: No API key configured', 'info');
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

// Handle drag and drop
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
        const fileInput = document.getElementById('bookFile');
        fileInput.files = files;
        handleFileUpload({ target: fileInput });
    }
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading('Uploading and parsing book...');
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showAlert(`✅ ${data.message}`, 'success');
            currentBookInfo = data.book_info;
            displayBookInfo(data.book_info);
            enableActions();
        } else {
            showAlert(`❌ Error: ${data.error || 'Upload failed'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Upload failed: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Handle URL load
async function handleUrlLoad() {
    const bookUrl = document.getElementById('bookUrl');
    const url = bookUrl.value.trim();
    
    if (!url) {
        showAlert('Please enter a URL', 'error');
        return;
    }
    
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        showAlert('Please enter a valid URL starting with http:// or https://', 'error');
        return;
    }
    
    showLoading('Downloading book from URL...');
    
    try {
        const formData = new FormData();
        formData.append('url', url);
        
        const response = await fetch('/api/load-from-url', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showAlert(`✅ ${data.message}`, 'success');
            currentBookInfo = data.book_info;
            displayBookInfo(data.book_info);
            enableActions();
            bookUrl.value = ''; // Clear URL input
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to load from URL'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Display book information
function displayBookInfo(bookInfo) {
    if (!bookInfo || !bookInfo.success) return;
    
    const bookInfoSection = document.getElementById('bookInfoSection');
    const bookInfoDiv = document.getElementById('bookInfo');
    const metadata = bookInfo.metadata;
    const chapters = bookInfo.chapters;
    
    currentChapters = chapters;
    
    // Update chapter select
    const chapterSelect = document.getElementById('chapterSelect');
    if (chapterSelect) {
        chapterSelect.innerHTML = '<option value="">All Chapters</option>';
        chapters.forEach(ch => {
            const option = document.createElement('option');
            option.value = ch.number;
            option.textContent = `Chapter ${ch.number}: ${ch.title}`;
            chapterSelect.appendChild(option);
        });
    }
    
    // Display book info
    bookInfoDiv.innerHTML = `
        <div class="book-info">
            <div class="info-item">
                <div class="info-label">Title</div>
                <div class="info-value">${metadata.title}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Author</div>
                <div class="info-value">${metadata.author}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Pages</div>
                <div class="info-value">${metadata.total_pages}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Chapters</div>
                <div class="info-value">${metadata.total_chapters}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Word Count</div>
                <div class="info-value">${metadata.word_count.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Reading Time</div>
                <div class="info-value">${metadata.estimated_reading_time.formatted}</div>
            </div>
        </div>
    `;
    
    // Display chapters
    const chaptersList = document.getElementById('chaptersList');
    if (chaptersList) {
        chaptersList.innerHTML = chapters.map(ch => `
            <div class="chapter-item" data-chapter-number="${ch.number}">
                <div class="chapter-header">
                    <div class="chapter-title">${ch.title}</div>
                    <div class="chapter-number">Chapter ${ch.number}</div>
                </div>
                <div class="chapter-word-count">${ch.word_count.toLocaleString()} words</div>
            </div>
        `).join('');
    }
    
    bookInfoSection.classList.remove('hidden');
    document.getElementById('chapterSection').classList.remove('hidden');
}

// Enable action buttons
function enableActions() {
    document.getElementById('actionsSection').classList.remove('hidden');
    document.getElementById('questionSection').classList.remove('hidden');
}

// Handle summarize all chapters
async function handleSummarizeAll() {
    showLoading('Generating summaries for all chapters...');
    
    try {
        const response = await fetch('/api/summarize-all', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults('Chapter Summaries', formatChapterSummaries(data.summaries));
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to generate summaries'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Handle summarize single chapter
async function handleSummarizeChapter(chapterNumber) {
    showLoading(`Generating summary for chapter ${chapterNumber}...`);
    
    try {
        const formData = new FormData();
        formData.append('chapter_number', chapterNumber);
        
        const response = await fetch('/api/summarize-chapter', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults(
                `Chapter ${data.chapter_number}: ${data.chapter_title}`,
                `<div class="summary-section">
                    <div class="summary-title">Summary</div>
                    <div>${data.summary}</div>
                </div>`
            );
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to generate summary'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Handle get takeaways
async function handleGetTakeaways() {
    showLoading('Extracting key takeaways...');
    
    try {
        const formData = new FormData();
        formData.append('num_takeaways', 10);
        
        const response = await fetch('/api/key-takeaways', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults('Key Takeaways', formatTakeaways(data.takeaways, data.formatted_text));
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to extract takeaways'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Handle get quotes
async function handleGetQuotes() {
    showLoading('Extracting important quotes...');
    
    try {
        const formData = new FormData();
        formData.append('num_quotes', 5);
        
        const response = await fetch('/api/get-quotes', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResults('Important Quotes', formatQuotes(data.quotes, data.formatted_text));
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to extract quotes'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Handle analyze book
async function handleAnalyzeBook() {
    showLoading('Performing full book analysis...');
    
    try {
        const formData = new FormData();
        formData.append('include_summaries', true);
        formData.append('include_takeaways', true);
        formData.append('include_quotes', true);
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            let content = '<div class="summary-section"><h3>Book Analysis Complete</h3></div>';
            
            if (data.chapter_summaries && data.chapter_summaries.success) {
                content += formatChapterSummaries(data.chapter_summaries.summaries);
            }
            
            if (data.key_takeaways && data.key_takeaways.success) {
                content += formatTakeaways(data.key_takeaways.takeaways, data.key_takeaways.formatted_text);
            }
            
            if (data.important_quotes && data.important_quotes.success) {
                content += formatQuotes(data.important_quotes.quotes, data.important_quotes.formatted_text);
            }
            
            displayResults('Full Book Analysis', content);
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to analyze book'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Handle ask question
async function handleAskQuestion() {
    const questionInput = document.getElementById('questionInput');
    const chapterSelect = document.getElementById('chapterSelect');
    const question = questionInput.value.trim();
    
    if (!question) {
        showAlert('Please enter a question', 'error');
        return;
    }
    
    showLoading('Answering your question...');
    
    try {
        const formData = new FormData();
        formData.append('question', question);
        if (chapterSelect.value) {
            formData.append('chapter_number', chapterSelect.value);
        }
        
        const response = await fetch('/api/ask-question', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            const answerDiv = document.getElementById('questionAnswer');
            answerDiv.innerHTML = `
                <div class="summary-section">
                    <div class="summary-title">Question: ${data.question}</div>
                    <div style="margin-top: 1rem;">${data.answer}</div>
                    ${data.chapter_context ? `<div style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-secondary);">Context: ${data.chapter_context}</div>` : ''}
                </div>
            `;
            answerDiv.classList.remove('hidden');
            questionInput.value = '';
        } else {
            showAlert(`❌ Error: ${data.error || 'Failed to answer question'}`, 'error');
        }
    } catch (error) {
        showAlert(`❌ Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Format chapter summaries
function formatChapterSummaries(summaries) {
    return summaries.map(s => `
        <div class="summary-section">
            <div class="summary-title">Chapter ${s.chapter_number}: ${s.chapter_title}</div>
            <div>${s.summary}</div>
        </div>
    `).join('');
}

// Format takeaways
function formatTakeaways(takeaways, formattedText) {
    if (takeaways && takeaways.length > 0) {
        return `
            <div class="summary-section">
                <div class="summary-title">Key Takeaways</div>
                <ol class="takeaways-list">
                    ${takeaways.map(t => `<li>${t}</li>`).join('')}
                </ol>
            </div>
        `;
    }
    return `
        <div class="summary-section">
            <div class="summary-title">Key Takeaways</div>
            <div>${formattedText}</div>
        </div>
    `;
}

// Format quotes
function formatQuotes(quotes, formattedText) {
    if (quotes && quotes.length > 0) {
        return `
            <div class="summary-section">
                <div class="summary-title">Important Quotes</div>
                <div class="quotes-list">
                    ${quotes.map(q => `
                        <div class="quote-item">
                            <div class="quote-text">"${q.quote}"</div>
                            ${q.context ? `<div class="quote-context">${q.context}</div>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    return `
        <div class="summary-section">
            <div class="summary-title">Important Quotes</div>
            <div>${formattedText}</div>
        </div>
    `;
}

// Display results
function displayResults(title, content) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsHeader = document.getElementById('resultsHeader');
    const resultsContent = document.getElementById('resultsContent');
    
    // Update header with title (keep clear button)
    const clearBtn = resultsHeader.querySelector('.btn-icon-only');
    resultsHeader.innerHTML = `<span>${title}</span>`;
    if (clearBtn) {
        resultsHeader.appendChild(clearBtn);
    } else {
        const btn = document.createElement('button');
        btn.className = 'btn-icon-only';
        btn.innerHTML = '✕';
        btn.title = 'Clear results';
        btn.addEventListener('click', () => {
            resultsSection.classList.add('hidden');
        });
        resultsHeader.appendChild(btn);
    }
    
    resultsContent.innerHTML = content;
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Show loading overlay
function showLoading(message = 'Processing...') {
    const overlay = document.getElementById('loadingOverlay');
    const messageEl = document.getElementById('loadingMessage');
    if (overlay) {
        if (messageEl) messageEl.textContent = message;
        overlay.classList.remove('hidden');
    }
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

// Show alert
function showAlert(message, type = 'info') {
    const uploadStatus = document.getElementById('uploadStatus');
    if (uploadStatus) {
        uploadStatus.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
        uploadStatus.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            uploadStatus.classList.add('hidden');
        }, 5000);
    }
}
