// CodeReviewerBot Frontend JavaScript
// Day 13 of #100DaysOfAI-Agents

class CodeReviewerApp {
    constructor() {
        this.currentInputMethod = null;
        this.currentResults = null;
        this.codeEditor = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupCodeEditor();
        this.setupFileUpload();
        this.setupGitHubValidation();
    }

    setupEventListeners() {
        // UI Language change
        document.getElementById('uiLanguage').addEventListener('change', (e) => {
            this.updateUILanguage(e.target.value);
        });

        // Review button
        document.getElementById('reviewBtn').addEventListener('click', () => {
            this.reviewCode();
        });
    }

    setupCodeEditor() {
        console.log('Setting up CodeMirror editor');
        const textarea = document.getElementById('codeInput');
        if (textarea) {
            console.log('Textarea found, initializing CodeMirror');
            this.codeEditor = CodeMirror.fromTextArea(textarea, {
                mode: 'javascript',
                theme: 'monokai',
                lineNumbers: true,
                autoCloseBrackets: true,
                matchBrackets: true,
                indentUnit: 4,
                tabSize: 4,
                lineWrapping: true,
                foldGutter: true,
                gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
                extraKeys: {
                    'Ctrl-Space': 'autocomplete'
                }
            });

            // Auto-detect language based on content
            this.codeEditor.on('change', () => {
                this.autoDetectLanguage();
            });
            
            console.log('CodeMirror editor initialized successfully');
        } else {
            console.error('Textarea with id "codeInput" not found');
        }
    }

    setupFileUpload() {
        const fileInput = document.getElementById('fileInput');
        const dropZone = document.querySelector('#fileInputForm .border-dashed');

        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                this.handleFileSelect(e.target.files[0]);
            });
        }

        if (dropZone) {
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('border-blue-400', 'bg-blue-50/10');
            });

            dropZone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                dropZone.classList.remove('border-blue-400', 'bg-blue-50/10');
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('border-blue-400', 'bg-blue-50/10');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileSelect(files[0]);
                }
            });
        }
    }

    setupGitHubValidation() {
        const githubUrlInput = document.getElementById('githubUrl');
        if (githubUrlInput) {
            let timeout;
            githubUrlInput.addEventListener('input', (e) => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    this.validateGitHubUrl(e.target.value);
                }, 1000);
            });
        }
    }

    selectInputMethod(method) {
        console.log('Selecting input method:', method);
        this.currentInputMethod = method;
        
        // Hide all forms
        document.getElementById('textInputForm').classList.add('hidden');
        document.getElementById('fileInputForm').classList.add('hidden');
        document.getElementById('githubInputForm').classList.add('hidden');
        
        // Show selected form
        const selectedForm = document.getElementById(`${method}InputForm`);
        if (selectedForm) {
            selectedForm.classList.remove('hidden');
            console.log(`Showing ${method}InputForm`);
        } else {
            console.error(`Form ${method}InputForm not found`);
        }
        
        // Update active state
        document.querySelectorAll('.glassmorphism').forEach(el => {
            el.classList.remove('ring-2', 'ring-blue-400');
        });
        event.currentTarget.classList.add('ring-2', 'ring-blue-400');
        
        // Initialize CodeMirror if text input is selected
        if (method === 'text' && !this.codeEditor) {
            console.log('Initializing CodeMirror editor');
            this.setupCodeEditor();
        }
    }

    async handleFileSelect(file) {
        if (!file) return;

        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileLanguage = document.getElementById('fileLanguage');

        // Validate file type
        const supportedExtensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.cs', '.php', '.go', '.rs', '.swift', '.kt', '.kts'];
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!supportedExtensions.includes(extension)) {
            this.showError('Unsupported file type. Please upload a supported code file.');
            return;
        }

        // Update UI
        fileName.textContent = file.name;
        fileLanguage.textContent = this.getLanguageName(extension);
        fileInfo.classList.remove('hidden');

        // Read file content
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            if (this.codeEditor) {
                this.codeEditor.setValue(content);
                this.autoDetectLanguage();
            }
        };
        reader.readAsText(file);
    }

    async validateGitHubUrl(url) {
        if (!url || !url.includes('github.com')) {
            document.getElementById('githubInfo').classList.add('hidden');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('github_url', url);

            const response = await fetch('/api/validate-github', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const githubInfo = document.getElementById('githubInfo');
            const repoInfo = document.getElementById('repoInfo');
            const fileInfo = document.getElementById('fileInfo');

            if (result.valid) {
                const info = result.github_info;
                if (info.type === 'file') {
                    repoInfo.textContent = `${info.owner}/${info.repo}`;
                    fileInfo.textContent = info.path;
                } else {
                    repoInfo.textContent = `${info.owner}/${info.repo}`;
                    fileInfo.textContent = 'Repository (will fetch first code file)';
                }
                githubInfo.classList.remove('hidden');
            } else {
                githubInfo.classList.add('hidden');
            }
        } catch (error) {
            console.error('GitHub validation error:', error);
        }
    }

    autoDetectLanguage() {
        if (!this.codeEditor) return;

        const content = this.codeEditor.getValue();
        const languageSelect = document.getElementById('languageSelect');

        // Simple language detection
        let detectedLanguage = '';
        if (content.includes('def ') || content.includes('import ') || content.includes('from ')) {
            detectedLanguage = 'python';
        } else if (content.includes('function') || content.includes('const ') || content.includes('let ')) {
            detectedLanguage = 'javascript';
        } else if (content.includes('public class') || content.includes('private ') || content.includes('public ')) {
            detectedLanguage = 'java';
        } else if (content.includes('#include') || content.includes('int main')) {
            detectedLanguage = 'cpp';
        } else if (content.includes('using ') || content.includes('namespace ')) {
            detectedLanguage = 'csharp';
        } else if (content.includes('<?php') || content.includes('function ')) {
            detectedLanguage = 'php';
        } else if (content.includes('package ') || content.includes('func ')) {
            detectedLanguage = 'go';
        } else if (content.includes('fn ') || content.includes('let ') || content.includes('mut ')) {
            detectedLanguage = 'rust';
        } else if (content.includes('import ') && content.includes('class ')) {
            detectedLanguage = 'swift';
        } else if (content.includes('fun ') || content.includes('val ') || content.includes('var ')) {
            detectedLanguage = 'kotlin';
        }

        if (detectedLanguage) {
            languageSelect.value = detectedLanguage;
            this.updateCodeEditorMode(detectedLanguage);
        }
    }

    updateCodeEditorMode(language) {
        if (!this.codeEditor) return;

        const modeMap = {
            'python': 'python',
            'javascript': 'javascript',
            'java': 'text/x-java-source',
            'cpp': 'text/x-c++src',
            'csharp': 'text/x-csharp',
            'php': 'php',
            'go': 'text/x-go',
            'rust': 'text/x-rustsrc',
            'swift': 'text/x-swift',
            'kotlin': 'text/x-kotlin'
        };

        const mode = modeMap[language] || 'javascript';
        this.codeEditor.setOption('mode', mode);
    }

    getLanguageName(extension) {
        const languageMap = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript (React)',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript (React)',
            '.java': 'Java',
            '.cpp': 'C++',
            '.cc': 'C++',
            '.cxx': 'C++',
            '.h': 'C++ Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.php': 'PHP',
            '.go': 'Go',
            '.rs': 'Rust',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.kts': 'Kotlin Script'
        };
        return languageMap[extension] || 'Unknown';
    }

    async reviewCode() {
        console.log('Review code called, currentInputMethod:', this.currentInputMethod);
        
        if (!this.currentInputMethod) {
            this.showError('Please select an input method first.');
            return;
        }

        this.showLoading(true);
        this.hideError();
        this.hideResults();

        try {
            const formData = new FormData();
            const uiLanguage = document.getElementById('uiLanguage').value;

            formData.append('ui_language', uiLanguage);

            switch (this.currentInputMethod) {
                case 'text':
                    console.log('Processing text input');
                    const code = this.codeEditor ? this.codeEditor.getValue() : '';
                    const language = document.getElementById('languageSelect').value;
                    
                    console.log('Code length:', code.length);
                    console.log('Selected language:', language);
                    
                    if (!code.trim()) {
                        throw new Error('Please enter some code to review.');
                    }
                    
                    formData.append('code', code);
                    if (language) {
                        formData.append('language', language);
                    }
                    break;

                case 'file':
                    const fileInput = document.getElementById('fileInput');
                    if (!fileInput.files[0]) {
                        throw new Error('Please select a file to upload.');
                    }
                    formData.append('file', fileInput.files[0]);
                    break;

                case 'github':
                    const githubUrl = document.getElementById('githubUrl').value;
                    if (!githubUrl.trim()) {
                        throw new Error('Please enter a GitHub URL.');
                    }
                    formData.append('github_url', githubUrl);
                    break;
            }

            const response = await fetch('/api/review', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.currentResults = result.data;
                this.displayResults(result.data);
            } else {
                throw new Error(result.error || 'Code review failed.');
            }

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(data) {
        this.updateSummaryCards(data);
        this.updateScoreCards(data);
        this.populateIssues(data.issues);
        this.populateSuggestions(data.suggestions);
        this.populateRefactoredCode(data.refactored_code, data.language);
        this.populateSummary(data.summary, data.statistics);
        
        document.getElementById('resultsContainer').classList.remove('hidden');
        document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth' });
    }

    updateSummaryCards(data) {
        const issues = data.statistics;
        document.getElementById('totalIssues').textContent = issues.total_issues;
        document.getElementById('criticalIssues').textContent = issues.critical_issues;
        
        // Count issues by severity
        const severityCounts = { high: 0, medium: 0, low: 0 };
        data.issues.forEach(issue => {
            if (issue.severity in severityCounts) {
                severityCounts[issue.severity]++;
            }
        });
        
        document.getElementById('highIssues').textContent = severityCounts.high;
        document.getElementById('mediumIssues').textContent = severityCounts.medium;
        document.getElementById('lowIssues').textContent = severityCounts.low;
    }

    updateScoreCards(data) {
        const scores = data.scores;
        document.getElementById('readabilityScore').textContent = scores.readability || '-';
        document.getElementById('qualityScore').textContent = scores.code_quality || '-';
        document.getElementById('performanceScore').textContent = scores.performance || '-';
        document.getElementById('bestPracticesScore').textContent = scores.best_practices || '-';
        document.getElementById('securityScore').textContent = scores.security || '-';
    }

    populateIssues(issues) {
        const issuesList = document.getElementById('issuesList');
        issuesList.innerHTML = '';

        if (issues.length === 0) {
            issuesList.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-check-circle text-green-400 text-4xl mb-4"></i>
                    <p class="text-white text-lg">No issues found! Your code looks great!</p>
                </div>
            `;
            return;
        }

        issues.forEach((issue, index) => {
            const issueElement = document.createElement('div');
            issueElement.className = `glassmorphism rounded-lg p-4 severity-${issue.severity}`;
            
            const severityIcon = this.getSeverityIcon(issue.severity);
            const categoryIcon = this.getCategoryIcon(issue.category);
            
            issueElement.innerHTML = `
                <div class="flex items-start justify-between">
                    <div class="flex items-center mb-2">
                        ${severityIcon}
                        <span class="ml-2 text-sm font-medium text-white bg-opacity-20 px-2 py-1 rounded">
                            ${issue.severity.toUpperCase()}
                        </span>
                        ${categoryIcon}
                        <span class="ml-2 text-sm text-blue-200">
                            ${issue.category.replace('_', ' ').toUpperCase()}
                        </span>
                        ${issue.line_number ? `<span class="ml-2 text-sm text-gray-300">Line ${issue.line_number}</span>` : ''}
                    </div>
                </div>
                <p class="text-white mb-2">${issue.message}</p>
                ${issue.code_snippet ? `
                    <div class="bg-gray-800 rounded p-3 mb-2">
                        <pre class="text-sm text-gray-300"><code>${this.escapeHtml(issue.code_snippet)}</code></pre>
                    </div>
                ` : ''}
                <div class="bg-blue-900 bg-opacity-30 rounded p-3">
                    <p class="text-blue-200 text-sm"><strong>Suggestion:</strong> ${issue.suggestion}</p>
                </div>
            `;
            
            issuesList.appendChild(issueElement);
        });
    }

    populateSuggestions(suggestions) {
        const suggestionsList = document.getElementById('suggestionsList');
        suggestionsList.innerHTML = '';

        if (suggestions.length === 0) {
            suggestionsList.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-lightbulb text-yellow-400 text-4xl mb-4"></i>
                    <p class="text-white text-lg">No general suggestions at this time.</p>
                </div>
            `;
            return;
        }

        // Render suggestions in a professional, structured way
        suggestions.forEach((suggestion, index) => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'glassmorphism rounded-lg p-5 shadow-lg';
            suggestionElement.innerHTML = `
                <div class="flex items-start">
                    <div class="flex-shrink-0">
                        <div class="w-9 h-9 rounded-full bg-yellow-500/20 flex items-center justify-center">
                            <i class="fas fa-lightbulb text-yellow-400"></i>
                        </div>
                    </div>
                    <div class="ml-4">
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-sm text-blue-200">Suggestion ${index + 1}</span>
                        </div>
                        <p class="text-white leading-relaxed">${suggestion}</p>
                    </div>
                </div>
            `;
            suggestionsList.appendChild(suggestionElement);
        });
    }

    populateRefactoredCode(code, language) {
        const container = document.getElementById('refactoredCodeContainer');
        
        if (!code) {
            container.innerHTML = `
                <div class="text-center py-8">
                    <i class="fas fa-code text-blue-400 text-4xl mb-4"></i>
                    <p class="text-white text-lg">No refactored code available.</p>
                </div>
            `;
            return;
        }

        // Create CodeMirror instance for refactored code
        const textarea = document.createElement('textarea');
        textarea.value = code;
        container.innerHTML = '';
        container.appendChild(textarea);

        const editor = CodeMirror.fromTextArea(textarea, {
            mode: this.getCodeMirrorMode(language),
            theme: 'monokai',
            lineNumbers: true,
            readOnly: true,
            lineWrapping: true
        });

        // Store editor reference for download
        this.refactoredCodeEditor = editor;
        // Ensure editor renders immediately (no hidden tab issue)
        setTimeout(() => editor.refresh(), 50);
    }

    populateSummary(summary, statistics) {
        const container = document.getElementById('summaryContent');
        
        const codeSummary = statistics.code_summary;
        const safeSummary = (summary && summary.trim().length)
            ? summary.replace(/\n/g, '<br>')
            : 'No detailed summary was provided by the AI for this snippet. The code appears simple; consider documenting intent and edge cases where applicable.';

        container.innerHTML = `
            <div class="space-y-6">
                <div class="glassmorphism rounded-lg p-6">
                    <h3 class="text-xl font-semibold text-white mb-4">
                        <i class="fas fa-chart-bar text-blue-300 mr-2"></i>
                        Code Analysis Summary
                    </h3>
                    <div class="grid md:grid-cols-2 gap-4 text-white">
                        <div>
                            <p><strong>Total Lines:</strong> ${codeSummary.total_lines}</p>
                            <p><strong>Code Lines:</strong> ${codeSummary.code_lines}</p>
                            <p><strong>Comment Lines:</strong> ${codeSummary.comment_lines}</p>
                            <p><strong>Comment Ratio:</strong> ${(codeSummary.comment_ratio * 100).toFixed(1)}%</p>
                        </div>
                        <div>
                            <p><strong>Functions:</strong> ${codeSummary.functions}</p>
                            <p><strong>Classes:</strong> ${codeSummary.classes}</p>
                            <p><strong>Imports:</strong> ${codeSummary.imports}</p>
                            <p><strong>Complexity:</strong> ${codeSummary.complexity}</p>
                        </div>
                    </div>
                </div>
                
                <div class="glassmorphism rounded-lg p-6">
                    <h3 class="text-xl font-semibold text-white mb-4">
                        <i class="fas fa-file-alt text-green-300 mr-2"></i>
                        Overall Assessment
                    </h3>
                    <div class="text-white leading-relaxed">
                        ${safeSummary}
                    </div>
                </div>
            </div>
        `;
    }

    getSeverityIcon(severity) {
        const icons = {
            'critical': '<i class="fas fa-exclamation-triangle text-red-400"></i>',
            'high': '<i class="fas fa-exclamation-circle text-yellow-400"></i>',
            'medium': '<i class="fas fa-info-circle text-blue-400"></i>',
            'low': '<i class="fas fa-info text-green-400"></i>'
        };
        return icons[severity] || icons['medium'];
    }

    getCategoryIcon(category) {
        const icons = {
            'syntax': '<i class="fas fa-bug text-red-400"></i>',
            'best_practices': '<i class="fas fa-book text-blue-400"></i>',
            'performance': '<i class="fas fa-tachometer-alt text-yellow-400"></i>',
            'security': '<i class="fas fa-shield-alt text-red-400"></i>',
            'readability': '<i class="fas fa-eye text-green-400"></i>'
        };
        return icons[category] || icons['best_practices'];
    }

    getCodeMirrorMode(language) {
        const modeMap = {
            'python': 'python',
            'javascript': 'javascript',
            'java': 'text/x-java-source',
            'cpp': 'text/x-c++src',
            'csharp': 'text/x-csharp',
            'php': 'php',
            'go': 'text/x-go',
            'rust': 'text/x-rustsrc',
            'swift': 'text/x-swift',
            'kotlin': 'text/x-kotlin'
        };
        return modeMap[language] || 'javascript';
    }

    showTab(tabName) {
        // Hide all tab contents
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.add('hidden');
        });

        // Remove active state from all tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('tab-active');
            btn.classList.add('text-blue-200');
        });

        // Show selected tab content
        document.getElementById(`${tabName}Tab`).classList.remove('hidden');

        // Add active state to selected tab button
        const activeBtn = event.currentTarget;
        activeBtn.classList.add('tab-active');
        activeBtn.classList.remove('text-blue-200');

        // Refresh CodeMirror instances when tab becomes visible
        if (tabName === 'refactored' && this.refactoredCodeEditor) {
            setTimeout(() => this.refactoredCodeEditor.refresh(), 50);
        }
    }

    downloadRefactoredCode() {
        if (!this.refactoredCodeEditor) {
            this.showError('No refactored code available to download.');
            return;
        }

        const code = this.refactoredCodeEditor.getValue();
        const language = this.currentResults?.language || 'txt';
        const extension = this.getFileExtension(language);
        const filename = `refactored_code.${extension}`;

        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    getFileExtension(language) {
        const extensions = {
            'python': 'py',
            'javascript': 'js',
            'java': 'java',
            'cpp': 'cpp',
            'csharp': 'cs',
            'php': 'php',
            'go': 'go',
            'rust': 'rs',
            'swift': 'swift',
            'kotlin': 'kt'
        };
        return extensions[language] || 'txt';
    }

    showLoading(show) {
        const loadingState = document.getElementById('loadingState');
        if (show) {
            loadingState.classList.remove('hidden');
        } else {
            loadingState.classList.add('hidden');
        }
    }

    showError(message) {
        const errorContainer = document.getElementById('errorContainer');
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
        errorContainer.scrollIntoView({ behavior: 'smooth' });
    }

    hideError() {
        document.getElementById('errorContainer').classList.add('hidden');
    }

    hideResults() {
        document.getElementById('resultsContainer').classList.add('hidden');
    }

    updateUILanguage(language) {
        // This could be expanded to support full internationalization
        console.log('UI Language changed to:', language);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.codeReviewerApp = new CodeReviewerApp();
});

// Global functions for HTML onclick handlers
function selectInputMethod(method) {
    window.codeReviewerApp.selectInputMethod(method);
}

function reviewCode() {
    window.codeReviewerApp.reviewCode();
}

function showTab(tabName) {
    window.codeReviewerApp.showTab(tabName);
}

function downloadRefactoredCode() {
    window.codeReviewerApp.downloadRefactoredCode();
}
