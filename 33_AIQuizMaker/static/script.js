/**
 * AI Quiz Maker - Frontend JavaScript
 * Handles all UI interactions, API calls, and dynamic content updates
 */

// Global variables
let currentQuiz = null;
let currentTab = 'topic';

// DOM elements
const elements = {
    // Navigation
    navBtns: document.querySelectorAll('.nav-btn'),
    
    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Input fields
    topicInput: document.getElementById('topic-input'),
    urlInput: document.getElementById('url-input'),
    fileInput: document.getElementById('file-input'),
    textInput: document.getElementById('text-input'),
    questionsInput: document.getElementById('questions-input'),
    difficultyInput: document.getElementById('difficulty-input'),
    includeAnswers: document.getElementById('include-answers'),
    
    // UI elements
    charCount: document.getElementById('char-count'),
    fileInfo: document.getElementById('file-info'),
    urlStatus: document.getElementById('url-status'),
    urlPreview: document.getElementById('url-preview'),
    urlContentPreview: document.getElementById('url-content-preview'),
    generateBtn: document.getElementById('generate-btn'),
    generationStatus: document.getElementById('generation-status'),
    quizDisplay: document.getElementById('quiz-display'),
    quizTitle: document.getElementById('quiz-title'),
    quizDifficulty: document.getElementById('quiz-difficulty'),
    quizQuestions: document.getElementById('quiz-questions'),
    quizModel: document.getElementById('quiz-model'),
    quizContent: document.getElementById('quiz-content'),
    
    // Sections
    sections: document.querySelectorAll('.section'),
    
    // History and stats
    historyList: document.getElementById('history-list'),
    statsContent: document.getElementById('stats-content'),
    
    // Overlays
    loadingOverlay: document.getElementById('loading-overlay'),
    toastContainer: document.getElementById('toast-container')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadHistory();
    loadStatistics();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Set up file drag and drop
    setupFileDragAndDrop();
    
    // Set up character counter
    setupCharacterCounter();
    
    // Show initial section
    showSection('generator');
    
    // Check API health
    checkAPIHealth();
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Navigation buttons
    elements.navBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            showSection(section);
        });
    });
    
    // Tab buttons
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            switchTab(tab);
        });
    });
    
    // File input change
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // Text input change
    elements.textInput.addEventListener('input', handleTextInput);
    
    // Generate button
    elements.generateBtn.addEventListener('click', generateQuiz);
}

/**
 * Set up file drag and drop
 */
function setupFileDragAndDrop() {
    const fileUpload = document.querySelector('.border-dashed');
    
    fileUpload.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.remove('border-gray-300');
        this.classList.add('border-blue-400', 'bg-blue-50');
    });
    
    fileUpload.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('border-blue-400', 'bg-blue-50');
        this.classList.add('border-gray-300');
    });
    
    fileUpload.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('border-blue-400', 'bg-blue-50');
        this.classList.add('border-gray-300');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            elements.fileInput.files = files;
            handleFileSelect();
        }
    });
}

/**
 * Set up character counter
 */
function setupCharacterCounter() {
    elements.textInput.addEventListener('input', function() {
        const count = this.value.length;
        elements.charCount.textContent = count;
        
        // Remove existing color classes
        elements.charCount.classList.remove('text-red-500', 'text-yellow-500', 'text-gray-500');
        
        if (count > 8000) {
            elements.charCount.classList.add('text-red-500');
        } else if (count > 5000) {
            elements.charCount.classList.add('text-yellow-500');
        } else {
            elements.charCount.classList.add('text-gray-500');
        }
    });
}

/**
 * Handle file selection
 */
function handleFileSelect() {
    const file = elements.fileInput.files[0];
    if (!file) return;
    
    // Validate file type
    const allowedTypes = ['.txt', '.md', '.doc', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showToast('error', 'Invalid file type', 'Please select a .txt, .md, .doc, or .docx file');
        return;
    }
    
    // Show file info
    elements.fileInfo.innerHTML = `
        <div class="flex items-center space-x-3">
            <i class="fas fa-file-alt text-blue-500 text-xl"></i>
            <span class="font-semibold text-gray-800">${file.name}</span>
            <span class="text-gray-500">(${(file.size / 1024).toFixed(1)} KB)</span>
        </div>
    `;
    elements.fileInfo.classList.remove('hidden');
    
    // Switch to text tab and populate with file content
    switchTab('text');
    
    // Read file content
    const reader = new FileReader();
    reader.onload = function(e) {
        elements.textInput.value = e.target.result;
        elements.textInput.dispatchEvent(new Event('input'));
    };
    reader.readAsText(file);
}

/**
 * Handle text input
 */
function handleTextInput() {
    // This is handled by the character counter setup
}

/**
 * Fetch content from URL
 */
async function fetchUrlContent() {
    const url = elements.urlInput.value.trim();
    
    if (!url) {
        showToast('error', 'No URL', 'Please enter a valid URL');
        return;
    }
    
    if (!isValidUrl(url)) {
        showToast('error', 'Invalid URL', 'Please enter a valid URL starting with http:// or https://');
        return;
    }
    
    try {
        // Show loading state
        elements.urlStatus.classList.remove('hidden');
        elements.urlPreview.classList.add('hidden');
        
        // Fetch content from URL
        const response = await fetch('/api/fetch-url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Show content preview
            elements.urlContentPreview.textContent = result.content.substring(0, 300) + (result.content.length > 300 ? '...' : '');
            elements.urlPreview.classList.remove('hidden');
            
            // Store the content for quiz generation
            window.urlContent = result.content;
            
            showToast('success', 'Content Fetched', 'Successfully retrieved content from URL');
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error fetching URL content:', error);
        showToast('error', 'Fetch Failed', error.message || 'Failed to fetch content from URL');
    } finally {
        elements.urlStatus.classList.add('hidden');
    }
}

/**
 * Validate URL format
 */
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

/**
 * Switch between input tabs
 */
function switchTab(tabName) {
    // Update tab buttons
    elements.tabBtns.forEach(btn => {
        if (btn.getAttribute('onclick').includes(tabName)) {
            btn.className = 'tab-btn bg-white text-blue-600 px-8 py-3 rounded-xl font-medium transition-all duration-200 shadow-md';
        } else {
            btn.className = 'tab-btn bg-transparent text-gray-600 hover:text-gray-800 px-8 py-3 rounded-xl font-medium transition-all duration-200';
        }
    });
    
    // Update tab content
    elements.tabContents.forEach(content => {
        if (content.id === `${tabName}-tab`) {
            content.classList.remove('hidden');
        } else {
            content.classList.add('hidden');
        }
    });
    
    currentTab = tabName;
}

/**
 * Show a specific section
 */
function showSection(sectionName) {
    // Update navigation buttons
    elements.navBtns.forEach(btn => {
        if (btn.getAttribute('onclick').includes(sectionName)) {
            btn.className = 'nav-btn bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-md';
        } else {
            btn.className = 'nav-btn bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-xl font-medium transition-all duration-200 transform hover:scale-105 active:scale-95';
        }
    });
    
    // Update sections
    elements.sections.forEach(section => {
        if (section.id === sectionName) {
            section.classList.remove('hidden');
        } else {
            section.classList.add('hidden');
        }
    });
    
    // Load section-specific content
    if (sectionName === 'history') {
        loadHistory();
    } else if (sectionName === 'stats') {
        loadStatistics();
    }
}

/**
 * Generate quiz
 */
async function generateQuiz() {
    try {
        // Get input content
        let content = '';
        if (currentTab === 'topic') {
            content = elements.topicInput.value.trim();
        } else if (currentTab === 'url') {
            if (!window.urlContent) {
                showToast('error', 'No URL Content', 'Please fetch content from a URL first');
                return;
            }
            content = window.urlContent;
        } else if (currentTab === 'text') {
            content = elements.textInput.value.trim();
        } else if (currentTab === 'file') {
            if (!elements.fileInput.files[0]) {
                showToast('error', 'No file selected', 'Please select a file to upload');
                return;
            }
            // For file upload, we need to read the file content
            const file = elements.fileInput.files[0];
            content = await readFileContent(file);
        }
        
        if (!content) {
            showToast('error', 'No content provided', 'Please enter a topic, upload a file, or paste text content');
            return;
        }
        
        // Validate input
        const validation = await validateInput(content);
        if (!validation.valid) {
            showToast('error', 'Invalid input', validation.errors.join(', '));
            return;
        }
        
        if (validation.warnings.length > 0) {
            showToast('warning', 'Warning', validation.warnings.join(', '));
        }
        
        // Get configuration
        const config = {
            content: content,
            questions: parseInt(elements.questionsInput.value),
            difficulty: elements.difficultyInput.value,
            include_answers: elements.includeAnswers.checked
        };
        
        // Show loading state
        setLoadingState(true);
        
        // Generate quiz
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentQuiz = result.quiz;
            
            // Debug: Log the quiz data
            console.log('🔍 Quiz data received:', result.quiz);
            console.log('🔍 Quiz structure:', {
                topic: result.quiz.topic,
                questions: result.quiz.questions,
                quiz: result.quiz.quiz,
                firstQuestion: result.quiz.quiz?.[0]
            });
            
            displayQuiz(result.quiz);
            showToast('success', 'Quiz Generated!', result.message);
            
            // Refresh history and stats
            loadHistory();
            loadStatistics();
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error generating quiz:', error);
        showToast('error', 'Generation Failed', error.message || 'Failed to generate quiz. Please try again.');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Read file content
 */
async function readFileContent(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsText(file);
    });
}

/**
 * Validate input before generation
 */
async function validateInput(content) {
    try {
        const response = await fetch('/api/validate-input', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                questions: parseInt(elements.questionsInput.value),
                difficulty: elements.difficultyInput.value
            })
        });
        
        const result = await response.json();
        return result;
        
    } catch (error) {
        console.error('Error validating input:', error);
        return { valid: false, errors: ['Validation failed'], warnings: [] };
    }
}

/**
 * Display the generated quiz
 */
function displayQuiz(quiz) {
    // Debug: Log what we're trying to display
    console.log('🔍 Displaying quiz:', quiz);
    console.log('🔍 Quiz.quiz array:', quiz.quiz);
    console.log('🔍 First question:', quiz.quiz?.[0]);
    
    // Update quiz header
    elements.quizTitle.textContent = quiz.topic;
    elements.quizDifficulty.textContent = quiz.difficulty.charAt(0).toUpperCase() + quiz.difficulty.slice(1);
    elements.quizQuestions.textContent = `${quiz.questions} Questions`;
    elements.quizModel.textContent = quiz.model;
    
    // Generate quiz content HTML
    let quizHTML = '';
    
    quiz.quiz.forEach((question, index) => {
        console.log(`🔍 Processing question ${index + 1}:`, question);
        console.log(`🔍 Question options:`, question.options);
        
        quizHTML += `
            <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-8 border border-blue-100 shadow-lg">
                <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-md">
                        ${index + 1}
                    </div>
                    <div class="flex-1">
                        <h4 class="text-xl font-semibold text-gray-800 mb-6 leading-relaxed">
                            ${question.question}
                        </h4>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        `;
        
        // Add options
        Object.entries(question.options).forEach(([letter, text]) => {
            console.log(`🔍 Adding option ${letter}: ${text}`);
            const isCorrect = quiz.include_answers && question.answer === letter;
            quizHTML += `
                <div class="flex items-center space-x-3 p-4 rounded-xl border-2 transition-all duration-200 ${isCorrect ? 'border-green-300 bg-green-50' : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50'}">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${isCorrect ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-700'}">
                        ${letter}
                    </div>
                    <span class="text-gray-700 font-medium">${text}</span>
                    ${isCorrect ? '<i class="fas fa-check-circle text-green-500 ml-auto"></i>' : ''}
                </div>
            `;
        });
        
        // Add answer if included
        if (quiz.include_answers && question.answer) {
            quizHTML += `
                        </div>
                        <div class="bg-green-100 border border-green-200 rounded-xl p-4">
                            <div class="flex items-center space-x-3">
                                <i class="fas fa-lightbulb text-green-600 text-xl"></i>
                                <div>
                                    <p class="font-semibold text-green-800">Correct Answer</p>
                                    <p class="text-green-700">Option ${question.answer}</p>
                                </div>
                            </div>
                        </div>
            `;
        } else {
            quizHTML += `
                        </div>
            `;
        }
        
        quizHTML += `
                    </div>
                </div>
            </div>
        `;
    });
    
    elements.quizContent.innerHTML = quizHTML;
    
    // Show quiz display
    elements.quizDisplay.classList.remove('hidden');
    
    // Scroll to quiz
    elements.quizDisplay.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Export quiz in specified format
 */
async function exportQuiz(format) {
    if (!currentQuiz) {
        showToast('error', 'No Quiz', 'Please generate a quiz first');
        return;
    }
    
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quiz: currentQuiz,
                format: format,
                filename: `quiz_${currentQuiz.topic.replace(/\s+/g, '_').toLowerCase()}`
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Download the file
            const link = document.createElement('a');
            link.href = `/downloads/${result.filename}`;
            link.download = result.filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            showToast('success', 'Export Successful', `Quiz exported as ${format.toUpperCase()}`);
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error exporting quiz:', error);
        showToast('error', 'Export Failed', error.message || 'Failed to export quiz');
    }
}

/**
 * Copy quiz to clipboard
 */
async function copyToClipboard() {
    if (!currentQuiz) {
        showToast('error', 'No Quiz', 'Please generate a quiz first');
        return;
    }
    
    try {
        // Get quiz content as text
        let textContent = `Quiz: ${currentQuiz.topic}\n`;
        textContent += `Difficulty: ${currentQuiz.difficulty}\n`;
        textContent += `Questions: ${currentQuiz.questions}\n\n`;
        
        currentQuiz.quiz.forEach((question, index) => {
            textContent += `${index + 1}. ${question.question}\n`;
            
            Object.entries(question.options).forEach(([letter, text]) => {
                textContent += `   ${letter}) ${text}\n`;
            });
            
            if (currentQuiz.include_answers && question.answer) {
                textContent += `   Answer: ${question.answer}\n`;
            }
            
            textContent += '\n';
        });
        
        // Copy to clipboard
        await navigator.clipboard.writeText(textContent);
        showToast('success', 'Copied!', 'Quiz copied to clipboard');
        
    } catch (error) {
        console.error('Error copying to clipboard:', error);
        showToast('error', 'Copy Failed', 'Failed to copy quiz to clipboard');
    }
}

/**
 * Load quiz history
 */
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const result = await response.json();
        
        if (result.success) {
            displayHistory(result.history);
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error loading history:', error);
        elements.historyList.innerHTML = '<p class="text-center text-gray-500 col-span-full py-8">Failed to load history</p>';
    }
}

/**
 * Display quiz history
 */
function displayHistory(history) {
    if (history.length === 0) {
        elements.historyList.innerHTML = `
            <div class="col-span-full text-center py-12">
                <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fas fa-history text-4xl text-gray-400"></i>
                </div>
                <p class="text-xl text-gray-600">No quiz history yet</p>
                <p class="text-gray-500 mt-2">Generate your first quiz to see it here!</p>
            </div>
        `;
        return;
    }
    
    let historyHTML = '';
    
    history.forEach(item => {
        const timestamp = new Date(item.timestamp).toLocaleString();
        
        historyHTML += `
            <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 cursor-pointer" onclick="loadQuizFromHistory('${item.id}')">
                <div class="flex items-start justify-between mb-4">
                    <div class="flex-1">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">${item.topic}</h3>
                        <div class="flex items-center space-x-4 text-sm text-gray-600">
                            <span class="flex items-center">
                                <i class="fas fa-question-circle text-blue-500 mr-2"></i>
                                ${item.questions} questions
                            </span>
                            <span class="flex items-center">
                                <i class="fas fa-signal text-green-500 mr-2"></i>
                                ${item.difficulty}
                            </span>
                        </div>
                    </div>
                    <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                        <i class="fas fa-quiz text-white text-lg"></i>
                    </div>
                </div>
                <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                    <span class="text-sm text-gray-500">${timestamp}</span>
                    <div class="flex space-x-2">
                        <button class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105" onclick="event.stopPropagation(); exportHistoryQuiz('${item.id}', 'md')">
                            <i class="fas fa-file-alt mr-1"></i> MD
                        </button>
                        <button class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105" onclick="event.stopPropagation(); exportHistoryQuiz('${item.id}', 'json')">
                            <i class="fas fa-code mr-1"></i> JSON
                        </button>
                        <button class="bg-orange-500 hover:bg-orange-600 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105" onclick="event.stopPropagation(); exportHistoryQuiz('${item.id}', 'csv')">
                            <i class="fas fa-table mr-1"></i> CSV
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    elements.historyList.innerHTML = historyHTML;
}

/**
 * Load quiz from history
 */
async function loadQuizFromHistory(quizId) {
    try {
        const response = await fetch(`/api/history/${quizId}`);
        const result = await response.json();
        
        if (result.success) {
            currentQuiz = result.quiz;
            displayQuiz(result.quiz);
            showSection('generator');
            showToast('success', 'Quiz Loaded', 'Quiz loaded from history');
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error loading quiz from history:', error);
        showToast('error', 'Load Failed', 'Failed to load quiz from history');
    }
}

/**
 * Export quiz from history
 */
async function exportHistoryQuiz(quizId, format) {
    try {
        const response = await fetch(`/api/history/${quizId}`);
        const result = await response.json();
        
        if (result.success) {
            await exportQuiz(format);
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error exporting history quiz:', error);
        showToast('error', 'Export Failed', 'Failed to export quiz from history');
    }
}

/**
 * Clear quiz history
 */
async function clearHistory() {
    if (!confirm('Are you sure you want to clear all quiz history? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear-history', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            loadHistory();
            loadStatistics();
            showToast('success', 'History Cleared', result.message);
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error clearing history:', error);
        showToast('error', 'Clear Failed', 'Failed to clear history');
    }
}

/**
 * Load statistics
 */
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const result = await response.json();
        
        if (result.success) {
            displayStatistics(result.statistics);
        } else {
            throw new Error(result.error);
        }
        
    } catch (error) {
        console.error('Error loading statistics:', error);
        elements.statsContent.innerHTML = '<p class="text-center text-gray-500 py-8">Failed to load statistics</p>';
    }
}

/**
 * Display statistics
 */
function displayStatistics(stats) {
    const lastGenerated = stats.last_generated ? new Date(stats.last_generated).toLocaleString() : 'Never';
    
    let statsHTML = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div class="text-center">
                <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fas fa-question-circle text-3xl text-blue-600"></i>
                </div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">Total Questions</h3>
                <p class="text-4xl font-bold text-blue-600">${stats.total_questions || 0}</p>
            </div>
            <div class="text-center">
                <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fas fa-magic text-3xl text-green-600"></i>
                </div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">Quizzes Generated</h3>
                <p class="text-4xl font-bold text-green-600">${stats.total_quizzes || 0}</p>
            </div>
            <div class="text-center">
                <div class="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fas fa-clock text-3xl text-purple-600"></i>
                </div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">Last Generated</h3>
                <p class="text-lg text-gray-600">${lastGenerated.split(',')[0]}</p>
            </div>
        </div>
        
        <div class="bg-gray-50 rounded-2xl p-8">
            <h4 class="text-2xl font-bold text-gray-800 mb-6 text-center">Difficulty Distribution</h4>
            <div class="space-y-6">
                <div class="flex items-center space-x-4">
                    <span class="w-20 text-sm font-semibold text-gray-700">Easy</span>
                    <div class="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                        <div class="bg-green-500 h-full rounded-full transition-all duration-500" style="width: ${(stats.difficulty_distribution?.easy / Math.max(stats.total_quizzes, 1)) * 100}%"></div>
                    </div>
                    <span class="w-16 text-right text-sm font-bold text-gray-800">${stats.difficulty_distribution?.easy || 0}</span>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="w-20 text-sm font-semibold text-gray-700">Medium</span>
                    <div class="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                        <div class="bg-blue-500 h-full rounded-full transition-all duration-500" style="width: ${(stats.difficulty_distribution?.medium / Math.max(stats.total_quizzes, 1)) * 100}%"></div>
                    </div>
                    <span class="w-16 text-right text-sm font-bold text-gray-800">${stats.difficulty_distribution?.medium || 0}</span>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="w-20 text-sm font-semibold text-gray-700">Hard</span>
                    <div class="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                        <div class="bg-red-500 h-full rounded-full transition-all duration-500" style="width: ${(stats.difficulty_distribution?.hard / Math.max(stats.total_quizzes, 1)) * 100}%"></div>
                    </div>
                    <span class="w-16 text-right text-sm font-bold text-gray-800">${stats.difficulty_distribution?.hard || 0}</span>
                </div>
            </div>
        </div>
    `;
    
    elements.statsContent.innerHTML = statsHTML;
}

/**
 * Check API health
 */
async function checkAPIHealth() {
    try {
        const response = await fetch('/api/health');
        const result = await response.json();
        
        if (result.status === 'healthy' && result.quiz_generator === 'ready') {
            console.log('API is healthy and ready');
        } else {
            console.warn('API health check failed:', result);
        }
        
    } catch (error) {
        console.error('API health check failed:', error);
    }
}

/**
 * Set loading state
 */
function setLoadingState(loading) {
    if (loading) {
        elements.loadingOverlay.classList.remove('hidden');
        elements.generateBtn.disabled = true;
        elements.generateBtn.className = 'bg-gray-400 cursor-not-allowed px-12 py-4 rounded-2xl font-bold text-xl shadow-lg';
        elements.generationStatus.classList.remove('hidden');
    } else {
        elements.loadingOverlay.classList.add('hidden');
        elements.generateBtn.disabled = false;
        elements.generateBtn.className = 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-12 py-4 rounded-2xl font-bold text-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl';
        elements.generationStatus.classList.add('hidden');
    }
}

/**
 * Show toast notification
 */
function showToast(type, title, message) {
    const toast = document.createElement('div');
    
    const typeClasses = {
        success: 'bg-green-500 border-green-600',
        error: 'bg-red-500 border-red-600',
        warning: 'bg-yellow-500 border-yellow-600',
        info: 'bg-blue-500 border-blue-600'
    };
    
    toast.className = `${typeClasses[type] || typeClasses.info} text-white border-l-4 rounded-lg shadow-lg p-4 min-w-80 transform transition-all duration-300 translate-x-full`;
    
    toast.innerHTML = `
        <div class="flex items-start justify-between">
            <div class="flex-1">
                <h4 class="font-semibold text-lg mb-1">${title}</h4>
                <p class="text-sm opacity-90">${message}</p>
            </div>
            <button class="ml-4 text-white hover:text-gray-200 transition-colors duration-200" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times text-lg"></i>
            </button>
        </div>
    `;
    
    elements.toastContainer.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        }
    }, 5000);
}

/**
 * Utility function to format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Utility function to debounce function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global access
window.showSection = showSection;
window.switchTab = switchTab;
window.generateQuiz = generateQuiz;
window.exportQuiz = exportQuiz;
window.copyToClipboard = copyToClipboard;
window.loadQuizFromHistory = loadQuizFromHistory;
window.exportHistoryQuiz = exportHistoryQuiz;
window.clearHistory = clearHistory;
window.fetchUrlContent = fetchUrlContent;
