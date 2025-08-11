// SpeechToTextAgent - Frontend Application Logic

class SpeechToTextApp {
    constructor() {
        this.currentInputMethod = null;
        this.selectedFile = null;
        this.youtubeUrl = null;
        this.transcriptionData = null;
        this.lastWarning = null;
        this.progressInterval = null;
        this.timerInterval = null;
        this.abortController = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.hideAllSections();
    }

    bindEvents() {
        // Input method selection
        document.getElementById('file-card').addEventListener('click', () => this.selectInputMethod('file'));
        document.getElementById('youtube-card').addEventListener('click', () => this.selectInputMethod('youtube'));
        document.getElementById('settings-card').addEventListener('click', () => this.toggleSettings());

        // File handling
        document.getElementById('file-input').addEventListener('change', (e) => this.handleFileSelect(e));
        
        // YouTube preview
        document.getElementById('youtube-url').addEventListener('input', (e) => this.handleYouTubeUrlInput(e));
        
        // Transcription
        document.getElementById('transcribe-btn').addEventListener('click', () => this.startTranscription());
    }

    selectInputMethod(method) {
        this.currentInputMethod = method;
        this.hideAllSections();
        
        // Update card styles
        document.querySelectorAll('.card').forEach(card => {
            card.style.transform = 'scale(1)';
            card.style.boxShadow = 'none';
        });
        
        const selectedCard = document.getElementById(`${method}-card`);
        selectedCard.style.transform = 'scale(1.05)';
        selectedCard.style.boxShadow = '0 20px 40px rgba(124, 58, 237, 0.3)';
        
        // Show appropriate form
        if (method === 'file') {
            document.getElementById('file-form').classList.remove('hidden');
        } else if (method === 'youtube') {
            document.getElementById('youtube-form').classList.remove('hidden');
        }
        
        // Show transcribe button if we have input
        this.updateTranscribeButton();
    }

    toggleSettings() {
        const settingsPanel = document.getElementById('settings-panel');
        const isHidden = settingsPanel.classList.contains('hidden');
        
        if (isHidden) {
            settingsPanel.classList.remove('hidden');
            settingsPanel.classList.add('fade-in');
        } else {
            settingsPanel.classList.add('hidden');
        }
    }

    hideAllSections() {
        const sections = ['file-form', 'youtube-form', 'settings-panel', 'progress-section', 'results-section', 'error-section'];
        sections.forEach(section => {
            document.getElementById(section).classList.add('hidden');
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.selectedFile = file;
            this.displayFileInfo(file);
            this.updateTranscribeButton();
        }
    }

    handleFileDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            this.selectedFile = file;
            this.displayFileInfo(file);
            this.updateTranscribeButton();
            
            // Update file input
            const fileInput = document.getElementById('file-input');
            fileInput.files = files;
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('dragover');
    }

    handleDragLeave(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
    }

    displayFileInfo(file) {
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');
        
        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        
        fileInfo.classList.remove('hidden');
        fileInfo.classList.add('fade-in');
    }

    removeFile() {
        this.selectedFile = null;
        document.getElementById('file-info').classList.add('hidden');
        document.getElementById('file-input').value = '';
        this.updateTranscribeButton();
    }

    handleYouTubeUrlInput(event) {
        this.youtubeUrl = event.target.value.trim();
        this.updateTranscribeButton();
        
        // Hide preview if URL is cleared
        if (!this.youtubeUrl) {
            document.getElementById('youtube-preview').classList.add('hidden');
        }
    }

    async previewYouTube() {
        const url = document.getElementById('youtube-url').value.trim();
        if (!url) {
            this.showError('Please enter a YouTube URL');
            return;
        }

        try {
            // Show loading state
            const previewBtn = event.target;
            const originalText = previewBtn.textContent;
            previewBtn.textContent = 'Loading...';
            previewBtn.disabled = true;

            // Get video info from backend (this would need a separate endpoint)
            // For now, we'll just validate the URL format
            if (this.isValidYouTubeUrl(url)) {
                this.showYouTubePreview({
                    title: 'Video Preview',
                    duration: 'Unknown',
                    uploader: 'Unknown',
                    thumbnail: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAyMCAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjIwIiBoZWlnaHQ9IjE2IiBmaWxsPSIjMzM0MTU1Ii8+CjxwYXRoIGQ9Ik04IDRMMTQgOEw4IDEyVjRaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K'
                });
            } else {
                this.showError('Invalid YouTube URL format');
            }
        } catch (error) {
            this.showError('Failed to preview YouTube video');
        } finally {
            previewBtn.textContent = originalText;
            previewBtn.disabled = false;
        }
    }

    isValidYouTubeUrl(url) {
        const youtubePatterns = [
            /youtube\.com\/watch\?v=/,
            /youtu\.be\//,
            /youtube\.com\/embed\//,
            /youtube\.com\/v\//,
            /youtube\.com\/shorts\//
        ];
        return youtubePatterns.some(pattern => pattern.test(url));
    }

    showYouTubePreview(videoInfo) {
        const preview = document.getElementById('youtube-preview');
        const thumbnail = document.getElementById('youtube-thumbnail');
        const title = document.getElementById('youtube-title');
        const duration = document.getElementById('youtube-duration');
        const uploader = document.getElementById('youtube-uploader');
        
        thumbnail.src = videoInfo.thumbnail;
        title.textContent = videoInfo.title;
        duration.textContent = videoInfo.duration;
        uploader.textContent = videoInfo.uploader;
        
        preview.classList.remove('hidden');
        preview.classList.add('fade-in');
    }

    updateTranscribeButton() {
        const transcribeBtn = document.getElementById('transcribe-btn');
        const hasInput = (this.currentInputMethod === 'file' && this.selectedFile) || 
                        (this.currentInputMethod === 'youtube' && this.youtubeUrl);
        
        if (hasInput) {
            transcribeBtn.classList.remove('hidden');
            transcribeBtn.classList.add('fade-in');
        } else {
            transcribeBtn.classList.add('hidden');
        }
    }

    async startTranscription() {
        try {
            // Reset warning state
            this.lastWarning = null;
            
            this.showProgress();
            this.hideAllSections();
            document.getElementById('progress-section').classList.remove('hidden');
            
            // Prepare form data
            const formData = new FormData();
            
            if (this.currentInputMethod === 'file' && this.selectedFile) {
                formData.append('file', this.selectedFile);
            } else if (this.currentInputMethod === 'youtube' && this.youtubeUrl) {
                formData.append('youtube_url', this.youtubeUrl);
            }
            
            // Add settings
            const language = document.getElementById('language-select').value;
            const includeTimestamps = document.getElementById('include-timestamps').checked;
            
            formData.append('language', language);
            formData.append('include_timestamps', includeTimestamps);
            
            // Start progress simulation
            this.simulateProgress();
            
            // Create AbortController for cancellation
            this.abortController = new AbortController();
            
            // Set timeout for the request (2 minutes)
            const timeoutDuration = 2 * 60 * 1000; // 2 minutes in milliseconds
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => {
                    this.abortController.abort();
                    reject(new Error('Request timed out after 2 minutes. Please try again.'));
                }, timeoutDuration);
            });
            
            // Send transcription request with timeout and abort controller
            const fetchPromise = fetch('/api/transcribe', {
                method: 'POST',
                body: formData,
                signal: this.abortController.signal
            });
            
            const response = await Promise.race([fetchPromise, timeoutPromise]);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Transcription failed');
            }
            
            const result = await response.json();
            this.showResults(result);
            
        } catch (error) {
            console.error('Transcription error:', error);
            if (error.name === 'AbortError') {
                this.showError('Transcription was cancelled or timed out');
            } else {
                this.showError(error.message);
            }
            // Reset progress on error
            this.resetProgress();
        }
    }

    simulateProgress() {
        const progressBar = document.getElementById('progress-bar');
        const progressPercentage = document.getElementById('progress-percentage');
        const progressStatus = document.getElementById('progress-status');
        const progressTimer = document.getElementById('progress-timer');
        
        const steps = [
            { percentage: 20, status: 'Processing file...' },
            { percentage: 40, status: 'Extracting audio...' },
            { percentage: 60, status: 'Sending to OpenAI...' },
            { percentage: 80, status: 'Transcribing...' },
            { percentage: 100, status: 'Finalizing...' }
        ];
        
        let currentStep = 0;
        let startTime = Date.now();
        
        // Clear any existing interval
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        this.progressInterval = setInterval(() => {
            if (currentStep < steps.length) {
                const step = steps[currentStep];
                progressBar.style.width = `${step.percentage}%`;
                progressPercentage.textContent = `${step.percentage}%`;
                progressStatus.textContent = step.status;
                currentStep++;
            } else {
                clearInterval(this.progressInterval);
            }
        }, 1000);
        
        // Update timer every second
        this.timerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            if (progressTimer) {
                progressTimer.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            }
            
            // Show timeout warnings
            if (elapsed >= 90) { // 1.5 minutes
                this.showTimeoutWarning('⚠️ Request taking longer than expected. Will timeout in 30 seconds.');
            } else if (elapsed >= 60) { // 1 minute
                this.showTimeoutWarning('⚠️ Request taking longer than expected. Will timeout in 1 minute.');
            } else if (elapsed >= 30) { // 30 seconds
                this.showTimeoutWarning('⚠️ Request taking longer than expected. Will timeout in 1.5 minutes.');
            }
        }, 1000);
    }

    resetProgress() {
        // Clear intervals
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        
        // Reset progress bar
        const progressBar = document.getElementById('progress-bar');
        const progressPercentage = document.getElementById('progress-percentage');
        const progressStatus = document.getElementById('progress-status');
        const progressTimer = document.getElementById('progress-timer');
        
        if (progressBar) progressBar.style.width = '0%';
        if (progressPercentage) progressPercentage.textContent = '0%';
        if (progressStatus) progressStatus.textContent = 'Ready';
        if (progressTimer) progressTimer.textContent = '0:00';
    }

    cancelTranscription() {
        // Abort the fetch request if it's running
        if (this.abortController) {
            this.abortController.abort();
        }
        
        // Clear intervals
        this.resetProgress();
        
        // Hide progress section
        document.getElementById('progress-section').classList.add('hidden');
        
        // Show error message
        this.showError('Transcription was cancelled by user');
        
        // Show toast
        this.showToast('Transcription cancelled', 'info');
    }

    showTimeoutWarning(message) {
        // Only show warning once per message
        if (this.lastWarning === message) return;
        this.lastWarning = message;
        
        this.showToast(message, 'error');
    }

    showProgress() {
        document.getElementById('progress-section').classList.remove('hidden');
        document.getElementById('progress-section').classList.add('fade-in');
    }

    showResults(data) {
        this.transcriptionData = data;
        
        // Update result fields
        const languageCode = data.language || 'unknown';
        const languageName = this.getLanguageName(languageCode);
        const nativeName = this.getNativeLanguageName(languageCode);
        
        document.getElementById('result-language').textContent = languageName;
        document.getElementById('result-language-native').textContent = nativeName;
        document.getElementById('result-duration').textContent = this.formatDuration(data.duration) || 'Unknown';
        document.getElementById('result-model').textContent = data.model || 'Unknown';
        document.getElementById('transcription-text').textContent = data.transcription || 'No transcription available';
        
        // Show results section
        this.hideAllSections();
        document.getElementById('results-section').classList.remove('hidden');
        document.getElementById('results-section').classList.add('fade-in');
    }

    getLanguageName(code) {
        const languages = {
            'auto': 'Auto-detect',
            'en': 'English',
            'hi': 'Hindi',
            'ur': 'Urdu',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'or': 'Odia',
            'as': 'Assamese',
            'ne': 'Nepali',
            'si': 'Sinhala',
            'my': 'Burmese',
            'km': 'Khmer',
            'lo': 'Lao',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'tl': 'Filipino',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'tr': 'Turkish',
            'nl': 'Dutch',
            'pl': 'Polish',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish',
            'unknown': 'Unknown'
        };
        return languages[code] || code;
    }

    getNativeLanguageName(code) {
        const nativeNames = {
            'auto': 'Auto-detect',
            'en': 'English',
            'hi': 'हिन्दी',
            'ur': 'اردو',
            'bn': 'বাংলা',
            'ta': 'தமிழ்',
            'te': 'తెలుగు',
            'kn': 'ಕನ್ನಡ',
            'ml': 'മലയാളം',
            'gu': 'ગુજરાતી',
            'pa': 'ਪੰਜਾਬੀ',
            'or': 'ଓଡ଼ିଆ',
            'as': 'অসমীয়া',
            'ne': 'नेपाली',
            'si': 'සිංහල',
            'my': 'မြန်မာ',
            'km': 'ខ្មែរ',
            'lo': 'ລາວ',
            'th': 'ไทย',
            'vi': 'Tiếng Việt',
            'id': 'Bahasa Indonesia',
            'ms': 'Bahasa Melayu',
            'tl': 'Filipino',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ja': '日本語',
            'ko': '한국어',
            'zh': '中文',
            'ar': 'العربية',
            'tr': 'Türkçe',
            'nl': 'Nederlands',
            'pl': 'Polski',
            'sv': 'Svenska',
            'da': 'Dansk',
            'no': 'Norsk',
            'fi': 'Suomi',
            'unknown': 'Unknown'
        };
        return nativeNames[code] || code;
    }

    showError(message) {
        document.getElementById('error-message').textContent = message;
        this.hideAllSections();
        document.getElementById('error-section').classList.remove('hidden');
        document.getElementById('error-section').classList.add('fade-in');
    }

    async copyToClipboard() {
        if (this.transcriptionData && this.transcriptionData.transcription) {
            try {
                await navigator.clipboard.writeText(this.transcriptionData.transcription);
                this.showToast('Text copied to clipboard!', 'success');
            } catch (error) {
                this.showToast('Failed to copy text', 'error');
            }
        }
    }

    downloadText() {
        if (this.transcriptionData && this.transcriptionData.transcription) {
            const blob = new Blob([this.transcriptionData.transcription], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `transcription_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.showToast('Text downloaded successfully!', 'success');
        }
    }

    resetForm() {
        this.selectedFile = null;
        this.youtubeUrl = null;
        this.transcriptionData = null;
        this.currentInputMethod = null;
        
        // Reset UI
        document.getElementById('file-input').value = '';
        document.getElementById('youtube-url').value = '';
        document.getElementById('language-select').value = 'auto';
        document.getElementById('include-timestamps').checked = false;
        
        this.hideAllSections();
        this.updateTranscribeButton();
        
        // Reset card styles
        document.querySelectorAll('.card').forEach(card => {
            card.style.transform = 'scale(1)';
            card.style.boxShadow = 'none';
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    formatDuration(seconds) {
        if (!seconds) return 'Unknown';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m ${remainingSeconds}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${remainingSeconds}s`;
        } else {
            return `${remainingSeconds}s`;
        }
    }

    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `fixed top-4 right-4 z-50 px-6 py-3 rounded-xl text-white font-medium transform translate-x-full transition-transform duration-300 ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 
            'bg-blue-500'
        }`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.transform = 'translateX(full)';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.speechToTextApp = new SpeechToTextApp();
});

// Global functions for HTML onclick handlers
function selectInputMethod(method) {
    window.speechToTextApp.selectInputMethod(method);
}

function toggleSettings() {
    window.speechToTextApp.toggleSettings();
}

function handleFileSelect(event) {
    window.speechToTextApp.handleFileSelect(event);
}

function handleFileDrop(event) {
    window.speechToTextApp.handleFileDrop(event);
}

function handleDragOver(event) {
    window.speechToTextApp.handleDragOver(event);
}

function handleDragLeave(event) {
    window.speechToTextApp.handleDragLeave(event);
}

function removeFile() {
    window.speechToTextApp.removeFile();
}

function handleYouTubeUrlInput(event) {
    window.speechToTextApp.handleYouTubeUrlInput(event);
}

function previewYouTube() {
    window.speechToTextApp.previewYouTube();
}

function startTranscription() {
    window.speechToTextApp.startTranscription();
}

function copyToClipboard() {
    window.speechToTextApp.copyToClipboard();
}

function downloadText() {
    window.speechToTextApp.downloadText();
}

function resetForm() {
    window.speechToTextApp.resetForm();
}

function cancelTranscription() {
    window.speechToTextApp.cancelTranscription();
}
