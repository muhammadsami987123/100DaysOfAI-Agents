// TranslatorAgent Web Interface JavaScript
class TranslatorApp {
    constructor() {
        this.currentTranslation = null;
        this.languages = [];
        this.history = [];
        this.isListening = false;
        this.isSpeaking = false;
        
        this.initializeElements();
        this.loadLanguages();
        this.loadHistory();
        this.setupEventListeners();
        this.createParticles();
    }

    initializeElements() {
        this.sourceLang = document.getElementById('sourceLang');
        this.targetLang = document.getElementById('targetLang');
        this.sourceText = document.getElementById('sourceText');
        this.translateBtn = document.getElementById('translateBtn');
        this.translationResult = document.getElementById('translationResult');
        this.translationText = document.getElementById('translationText');
        this.pronunciation = document.getElementById('pronunciation');
        this.loading = document.getElementById('loading');
        this.error = document.getElementById('error');
        this.copyBtn = document.getElementById('copyBtn');
        this.speakBtn = document.getElementById('speakBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.voiceEnabled = document.getElementById('voiceEnabled');
        this.listenBtn = document.getElementById('listenBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.historyContainer = document.getElementById('history');
    }

    async loadLanguages() {
        try {
            const response = await fetch('/api/languages');
            const data = await response.json();
            
            if (data.success) {
                this.languages = data.languages;
                this.populateLanguageDropdowns();
            }
        } catch (error) {
            console.error('Error loading languages:', error);
        }
    }

    populateLanguageDropdowns() {
        // Populate source language dropdown
        this.languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = `${lang.name} (${lang.native})`;
            option.className = 'text-gray-800';
            this.sourceLang.appendChild(option);
        });

        // Populate target language dropdown
        this.languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = `${lang.name} (${lang.native})`;
            option.className = 'text-gray-800';
            this.targetLang.appendChild(option);
        });
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            
            if (data.success) {
                this.history = data.history;
                this.updateHistoryDisplay();
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    updateHistoryDisplay() {
        if (this.history.length === 0) {
            this.historyContainer.innerHTML = '<p class="text-muted text-center font-medium">No recent translations</p>';
            return;
        }

        const historyHTML = this.history.slice(-5).reverse().map(entry => `
            <div class="glass rounded-lg p-3 shadow-md">
                <div class="text-secondary text-sm font-medium">${entry.timestamp}</div>
                <div class="text-primary font-semibold">${entry.original_text.substring(0, 50)}...</div>
                <div class="text-secondary">${entry.translation.substring(0, 50)}...</div>
                <div class="text-muted text-xs font-medium">${entry.source_lang} → ${entry.target_lang}</div>
            </div>
        `).join('');

        this.historyContainer.innerHTML = historyHTML;
    }

    setupEventListeners() {
        // Translate button
        this.translateBtn.addEventListener('click', () => this.translate());

        // Enter key in textarea
        this.sourceText.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.translate();
            }
        });

        // Copy button
        this.copyBtn.addEventListener('click', () => this.copyTranslation());

        // Speak button
        this.speakBtn.addEventListener('click', () => this.speakTranslation());

        // Download button
        this.downloadBtn.addEventListener('click', () => this.downloadTranslation());

        // Listen button
        this.listenBtn.addEventListener('click', () => this.startListening());

        // Stop button
        this.stopBtn.addEventListener('click', () => this.stopListening());

        // Quick action buttons
        document.querySelectorAll('.quick-action').forEach(btn => {
            btn.addEventListener('click', () => {
                this.sourceText.value = btn.dataset.text;
                this.translate();
            });
        });
    }

    async translate() {
        const text = this.sourceText.value.trim();
        if (!text) {
            this.showError('Please enter text to translate');
            return;
        }

        this.showLoading();
        this.hideError();

        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    source_lang: this.sourceLang.value,
                    target_lang: this.targetLang.value,
                    voice_enabled: this.voiceEnabled.checked
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentTranslation = data;
                this.showTranslation(data);
                this.loadHistory(); // Refresh history
            } else {
                this.showError(data.error || 'Translation failed');
            }
        } catch (error) {
            console.error('Translation error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    showTranslation(data) {
        this.translationText.textContent = data.translation;
        
        if (data.pronunciation) {
            this.pronunciation.textContent = `Pronunciation: ${data.pronunciation}`;
            this.pronunciation.style.display = 'block';
        } else {
            this.pronunciation.style.display = 'none';
        }

        this.translationResult.classList.remove('hidden');
        this.translationResult.scrollIntoView({ behavior: 'smooth' });
    }

    async copyTranslation() {
        if (!this.currentTranslation) return;

        try {
            await navigator.clipboard.writeText(this.currentTranslation.translation);
            this.showToast('Translation copied to clipboard!', 'success');
        } catch (error) {
            console.error('Copy error:', error);
            this.showError('Failed to copy translation');
        }
    }

    async speakTranslation() {
        if (!this.currentTranslation) {
            this.showError('No translation to speak');
            return;
        }

        if (this.isSpeaking) {
            this.showToast('Already speaking...', 'info');
            return;
        }

        try {
            // Update button state
            this.isSpeaking = true;
            this.speakBtn.disabled = true;
            this.speakBtn.textContent = '🔊 Speaking...';
            this.speakBtn.classList.add('opacity-50');

            console.log('Sending speech request:', {
                text: this.currentTranslation.translation,
                language: this.currentTranslation.target_lang
            });

            const response = await fetch('/api/voice/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: this.currentTranslation.translation,
                    language: this.currentTranslation.target_lang
                })
            });

            const data = await response.json();
            console.log('Speech response:', data);

            if (data.success) {
                this.showToast('Speaking translation...', 'success');
                
                // Wait a bit for speech to start, then reset button
                setTimeout(() => {
                    this.resetSpeakButton();
                }, 2000);
            } else {
                this.showError(data.error || 'Failed to speak translation');
                this.resetSpeakButton();
            }
        } catch (error) {
            console.error('Speak error:', error);
            this.showError('Failed to speak translation. Check console for details.');
            this.resetSpeakButton();
        }
    }

    resetSpeakButton() {
        this.isSpeaking = false;
        this.speakBtn.disabled = false;
        this.speakBtn.textContent = '🔊 Speak';
        this.speakBtn.classList.remove('opacity-50');
    }

    async startListening() {
        if (this.isListening) return;

        this.isListening = true;
        this.listenBtn.style.display = 'none';
        this.stopBtn.style.display = 'inline-block';
        this.showToast('Listening... Speak now', 'info');

        try {
            const response = await fetch('/api/voice/listen', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    language: this.sourceLang.value === 'auto' ? 'en' : this.sourceLang.value,
                    timeout: 10
                })
            });

            const data = await response.json();

            if (data.success) {
                this.sourceText.value = data.text;
                this.showToast('Speech recognized!', 'success');
            } else {
                this.showError(data.error || 'Failed to recognize speech');
            }
        } catch (error) {
            console.error('Listen error:', error);
            this.showError('Failed to start listening');
        } finally {
            this.stopListening();
        }
    }

    async stopListening() {
        this.isListening = false;
        this.listenBtn.style.display = 'inline-block';
        this.stopBtn.style.display = 'none';

        try {
            await fetch('/api/voice/stop', {
                method: 'POST'
            });
        } catch (error) {
            console.error('Stop listening error:', error);
        }
    }

    downloadTranslation() {
        if (!this.currentTranslation) return;

        const content = `Translation
Original: ${this.currentTranslation.original_text}
Translation: ${this.currentTranslation.translation}
From: ${this.currentTranslation.source_name} → To: ${this.currentTranslation.target_name}
Timestamp: ${new Date().toISOString()}`;

        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'translation.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showToast('Translation downloaded!', 'success');
    }

    showLoading() {
        this.loading.classList.remove('hidden');
        this.translateBtn.disabled = true;
    }

    hideLoading() {
        this.loading.classList.add('hidden');
        this.translateBtn.disabled = false;
    }

    showError(message) {
        this.error.classList.remove('hidden');
        this.error.querySelector('p').textContent = message;
    }

    hideError() {
        this.error.classList.add('hidden');
    }

    showToast(message, type = 'success') {
        // Create toast notification with improved styling
        const toast = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-500' : 
                       type === 'error' ? 'bg-red-500' : 
                       type === 'info' ? 'bg-blue-500' : 'bg-green-500';
        
        toast.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-slide-up font-medium`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    createParticles() {
        const particlesContainer = document.getElementById('particles');
        const particleCount = 50;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 6 + 's';
            particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
            particlesContainer.appendChild(particle);
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TranslatorApp();
}); 