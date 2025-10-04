// Frontend JavaScript for AIQuoteGenerator
class QuoteApp {
    constructor() {
        this.quoteForm = document.getElementById('quoteForm');
        this.moodSelect = document.getElementById('moodSelect');
        this.toneSelect = document.getElementById('toneSelect');
        this.outputFormatSelect = document.getElementById('outputFormatSelect');
        this.generateBtn = document.getElementById('generateBtn');
        this.btnText = document.getElementById('btnText');
        this.btnSpinner = document.getElementById('btnSpinner');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.quoteDisplay = document.getElementById('quoteDisplay');
        this.generatedQuote = document.getElementById('generatedQuote');
        this.quoteBackground = document.getElementById('quoteBackground');
        this.copyBtn = document.getElementById('copyBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.shareBtn = document.getElementById('shareBtn');
        this.errorDisplay = document.getElementById('errorDisplay');
        this.errorMessage = document.getElementById('errorMessage');
        this.quoteImageArea = document.getElementById('quoteImageArea');
        this.quoteOverlay = document.getElementById('quoteOverlay');

        this.isLoading = false;

        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.quoteForm.addEventListener('submit', this.handleFormSubmit.bind(this));
        this.copyBtn.addEventListener('click', this.copyQuote.bind(this));
        this.downloadBtn.addEventListener('click', this.downloadQuote.bind(this));
        this.shareBtn.addEventListener('click', this.shareQuote.bind(this));
        this.outputFormatSelect.addEventListener('change', this.handleOutputFormatChange.bind(this));
    }

    handleOutputFormatChange() {
        // Toggle image/text mode immediately on dropdown change
        const format = this.outputFormatSelect.value;
        if (format === 'Image Quote') {
            this.quoteBackground.style.opacity = '1';
            this.quoteOverlay.style.background = 'rgba(24,24,27,0.25)';
            this.generatedQuote.style.color = '#FFD700';
            this.generatedQuote.style.textShadow = '2px 2px 8px #18181b, 0 0 2px #FFD700';
        } else {
            this.quoteBackground.style.opacity = '0';
            this.quoteOverlay.style.background = 'none';
            this.generatedQuote.style.color = '#FFD700';
            this.generatedQuote.style.textShadow = '2px 2px 8px #18181b, 0 0 2px #FFD700';
        }
    }

    async handleFormSubmit(event) {
        event.preventDefault();
        if (this.isLoading) return;

        const mood = this.moodSelect.value;
        const tone = this.toneSelect.value;
        const output_format = this.outputFormatSelect.value;

        this.setLoading(true);
        this.hideDisplays();

        try {
            const response = await fetch('/api/generate_quote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mood, tone, output_format }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate quote.');
            }

            const data = await response.json();

            if (data.success) {
                this.displayQuote(data);
            } else {
                this.showError(data.error || 'Unknown error occurred.');
            }
        } catch (error) {
            this.showError(error.message || 'Network error. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        if (loading) {
            this.generateBtn.disabled = true;
            this.btnText.textContent = 'Crafting inspiration...';
            this.btnSpinner.classList.remove('hidden');
            this.loadingOverlay.classList.remove('hidden');
        } else {
            this.generateBtn.disabled = false;
            this.btnText.textContent = 'Generate Quote';
            this.btnSpinner.classList.add('hidden');
            this.loadingOverlay.classList.add('hidden');
        }
    }

    hideDisplays() {
        this.quoteDisplay.classList.add('hidden');
        this.errorDisplay.classList.add('hidden');
    }

    displayQuote(data) {
        this.generatedQuote.textContent = `"${data.quote}"`;
        let imgUrl = data.image_url;
        if (imgUrl && imgUrl.includes('unsplash.com')) {
            const cacheBuster = `t=${Date.now()}`;
            imgUrl += (imgUrl.includes('?') ? '&' : '?') + cacheBuster;
        }
        this.quoteBackground.src = imgUrl;
        // Show/hide image and overlay based on output format
        const format = this.outputFormatSelect.value;
        if (format === 'Image Quote') {
            this.quoteBackground.style.opacity = '1';
            this.quoteOverlay.style.background = 'rgba(24,24,27,0.25)';
            this.generatedQuote.style.color = '#FFD700';
            this.generatedQuote.style.textShadow = '2px 2px 8px #18181b, 0 0 2px #FFD700';
        } else {
            this.quoteBackground.style.opacity = '0';
            this.quoteOverlay.style.background = 'none';
            this.generatedQuote.style.color = '#FFD700';
            this.generatedQuote.style.textShadow = '2px 2px 8px #18181b, 0 0 2px #FFD700';
        }

        this.downloadBtn.style.display = (format === 'Image Quote') ? 'inline-flex' : 'none';
        this.shareBtn.style.display = (this.outputFormatSelect.value === 'Tweet-ready') ? 'inline-flex' : 'none';
        this.copyBtn.style.display = 'inline-flex';

        if (this.outputFormatSelect.value === 'Tweet-ready') {
            const tweetText = encodeURIComponent(data.tweet_ready);
            this.shareBtn.href = `https://twitter.com/intent/tweet?text=${tweetText}`;
        } else {
            this.shareBtn.removeAttribute('href');
        }

        this.quoteDisplay.classList.remove('hidden');
        this.quoteDisplay.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    showTooltip(btn, message) {
        const old = btn.parentElement.querySelector('.btn-tooltip');
        if (old) old.remove();
        const tooltip = document.createElement('span');
        tooltip.className = 'btn-tooltip absolute z-50 px-3 py-1 rounded-lg gold-gradient text-dark2 font-bold text-xs shadow-gold animate-fade-in';
        tooltip.style.top = '-2.5rem';
        tooltip.style.left = '50%';
        tooltip.style.transform = 'translateX(-50%)';
        tooltip.textContent = message;
        btn.parentElement.style.position = 'relative';
        btn.parentElement.appendChild(tooltip);
        setTimeout(() => {
            tooltip.classList.add('opacity-0');
            setTimeout(() => tooltip.remove(), 400);
        }, 1200);
    }

    goldGlowEffect(btn) {
        btn.classList.add('ring-4', 'ring-gold', 'ring-opacity-60');
        setTimeout(() => {
            btn.classList.remove('ring-4', 'ring-gold', 'ring-opacity-60');
        }, 400);
    }

    copyQuote() {
        const quoteText = this.generatedQuote.textContent.replace(/^"|"$/g, '');
        navigator.clipboard.writeText(quoteText)
            .then(() => {
                this.goldGlowEffect(this.copyBtn);
                this.showTooltip(this.copyBtn, 'Copied!');
            })
            .catch(err => {
                this.showTooltip(this.copyBtn, 'Failed!');
                console.error('Failed to copy quote: ', err);
            });
    }

    async downloadQuote() {
        const format = this.outputFormatSelect.value;
        if (format === 'Image Quote') {
            // Download the quote+image as PNG using html2canvas
            if (window.html2canvas) {
                const area = this.quoteImageArea;
                // Temporarily ensure image is visible for capture
                this.quoteBackground.style.opacity = '1';
                this.quoteOverlay.style.background = 'rgba(24,24,27,0.25)';
                await new Promise(r => setTimeout(r, 100)); // Wait for DOM update
                window.html2canvas(area, {useCORS: true, backgroundColor: null}).then(canvas => {
                    const link = document.createElement('a');
                    link.href = canvas.toDataURL('image/png');
                    link.download = 'ai_quote.png';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
            } else {
                alert('Image download not supported. Please try a modern browser.');
            }
        } else {
            // For text mode, fallback to copying text or a simple download
            this.copyQuote();
        }
    }

    shareQuote() {
        this.goldGlowEffect(this.shareBtn);
        this.showTooltip(this.shareBtn, 'Ready to Share!');
        if (this.outputFormatSelect.value !== 'Tweet-ready') {
            this.showTooltip(this.shareBtn, 'Share is for Tweet-ready');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new QuoteApp();
});
