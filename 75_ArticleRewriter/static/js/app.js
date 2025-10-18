/**
 * ArticleRewriter Frontend JavaScript
 */

class ArticleRewriterApp {
    constructor() {
        this.currentRewrite = null;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupExampleCards();
        this.setupWordCount();
        this.setupModals();
        this.setupAnimations();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('rewriteForm');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Submit button click (backup)
        const submitBtn = document.getElementById('rewriteBtn');
        submitBtn.addEventListener('click', (e) => {
            console.log('Submit button clicked!'); // Debug log
            // Let the form handle the submission
        });

        // Copy buttons
        document.getElementById('copyMain').addEventListener('click', () => this.copyToClipboard('mainRewrite'));
        document.getElementById('downloadMain').addEventListener('click', () => this.downloadContent('mainRewrite'));

        // Content input changes
        const contentTextarea = document.getElementById('content');
        contentTextarea.addEventListener('input', () => this.updateWordCount());
    }

    setupExampleCards() {
        const exampleCards = document.querySelectorAll('.example-card');
        exampleCards.forEach(card => {
            card.addEventListener('click', () => {
                const content = card.dataset.content;
                document.getElementById('content').value = content;
                this.updateWordCount();
                this.showToast('Example loaded!', 'info');
            });
        });
    }

    loadExample(type) {
        const examples = {
            'casual-to-formal': {
                content: "Hey! The weather is really nice today. I think we should go for a walk in the park. It would be fun!",
                tone: "formal",
                language: "english"
            },
            'professional-to-witty': {
                content: "Our company has achieved significant growth this quarter. We increased revenue by 25% and expanded our customer base by 40%.",
                tone: "witty",
                language: "english"
            },
            'technical-to-simplified': {
                content: "The new software update includes several bug fixes and performance improvements. Users will notice faster loading times and fewer crashes.",
                tone: "simplified",
                language: "english"
            }
        };

        const example = examples[type];
        if (example) {
            document.getElementById('content').value = example.content;
            document.getElementById('tone').value = example.tone;
            document.getElementById('language').value = example.language;
            this.updateWordCount();
            this.showToast('Example loaded!', 'success');
        }
    }

    setupWordCount() {
        this.updateWordCount();
    }

    setupModals() {
        // Welcome modal
        const welcomeModal = document.getElementById('welcomeModal');
        const closeWelcome = document.getElementById('closeWelcome');
        const aboutModal = document.getElementById('aboutModal');
        const aboutBtn = document.getElementById('aboutBtn');
        const closeAbout = document.getElementById('closeAbout');

        // Close welcome modal
        if (closeWelcome) {
            closeWelcome.addEventListener('click', () => {
                welcomeModal.style.display = 'none';
            });
        }

        // About modal
        if (aboutBtn) {
            aboutBtn.addEventListener('click', () => {
                aboutModal.classList.remove('hidden');
            });
        }

        if (closeAbout) {
            closeAbout.addEventListener('click', () => {
                aboutModal.classList.add('hidden');
            });
        }

        // Chatbot button
        const chatbotBtn = document.getElementById('chatbotBtn');
        if (chatbotBtn) {
            chatbotBtn.addEventListener('click', () => {
                this.showChatbot();
            });
        }

        // Close modals on backdrop click
        [welcomeModal, aboutModal].forEach(modal => {
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        modal.style.display = 'none';
                        modal.classList.add('hidden');
                    }
                });
            }
        });
    }

    setupAnimations() {
        // Add loading shimmer effect
        const loadingElements = document.querySelectorAll('.loading-shimmer');
        loadingElements.forEach(el => {
            el.classList.add('loading-shimmer');
        });

        // Add hover effects to cards
        const cards = document.querySelectorAll('.card-hover');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    updateWordCount() {
        const content = document.getElementById('content').value;
        const words = content.trim().split(/\s+/).filter(word => word.length > 0).length;
        const chars = content.length;
        
        document.getElementById('wordCount').textContent = words;
        document.getElementById('charCount').textContent = chars;
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        console.log('Form submitted!'); // Debug log
        
        const content = document.getElementById('content').value.trim();
        const tone = document.getElementById('tone').value;
        const language = document.getElementById('language').value;
        const generateVariations = document.getElementById('generateVariations').checked;

        console.log('Form data:', { content, tone, language, generateVariations }); // Debug log

        if (!content) {
            this.showToast('Please enter some content to rewrite', 'error');
            return;
        }

        await this.rewriteContent(content, tone, language, generateVariations);
    }

    async rewriteContent(content, tone, language, generateVariations) {
        this.setLoading(true);
        this.hideResults();

        try {
            const response = await fetch('/api/rewrite', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content,
                    tone,
                    language,
                    generate_variations: generateVariations
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.currentRewrite = data;
                this.displayResults(data);
                this.showToast('Content rewritten successfully!', 'success');
            } else {
                this.showToast(data.error || 'Failed to rewrite content', 'error');
            }

        } catch (error) {
            console.error('Error rewriting content:', error);
            this.showToast(error.message || 'Network error. Please try again.', 'error');
        } finally {
            this.setLoading(false);
        }
    }

    displayResults(data) {
        // Display main rewrite
        const mainRewrite = document.getElementById('mainRewrite');
        mainRewrite.textContent = data.rewritten_content;
        
        // Display variations if available
        const variationsSection = document.getElementById('variationsSection');
        const variationsContainer = document.getElementById('variationsContainer');
        
        if (data.variations && data.variations.length > 0) {
            variationsContainer.innerHTML = '';
            
            data.variations.forEach((variation, index) => {
                const variationCard = this.createVariationCard(variation, index + 1);
                variationsContainer.appendChild(variationCard);
            });
            
            variationsSection.classList.remove('hidden');
        } else {
            variationsSection.classList.add('hidden');
        }

        // Show results section
        document.getElementById('resultsSection').classList.remove('hidden');
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    createVariationCard(content, index) {
        const card = document.createElement('div');
        card.className = 'glass-effect rounded-xl p-6 shadow-lg animate-fade-in';
        
        card.innerHTML = `
            <div class="flex items-center justify-between mb-4">
                <h4 class="text-white font-semibold text-lg">Variation ${index}</h4>
                <div class="flex space-x-2">
                    <button class="copy-variation bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-lg transition-all duration-300 text-sm" data-content="${this.escapeHtml(content)}">
                        <i class="fas fa-copy mr-1"></i>Copy
                    </button>
                    <button class="download-variation bg-white/20 hover:bg-white/30 text-white px-3 py-1 rounded-lg transition-all duration-300 text-sm" data-content="${this.escapeHtml(content)}">
                        <i class="fas fa-download mr-1"></i>Download
                    </button>
                </div>
            </div>
            <div class="variation-content bg-white/10 rounded-lg p-4 text-white leading-relaxed whitespace-pre-wrap text-sm">${content}</div>
        `;

        // Add event listeners for copy and download buttons
        const copyBtn = card.querySelector('.copy-variation');
        const downloadBtn = card.querySelector('.download-variation');
        
        copyBtn.addEventListener('click', () => this.copyToClipboard(null, content));
        downloadBtn.addEventListener('click', () => this.downloadContent(null, content));

        return card;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async copyToClipboard(elementId, content = null) {
        try {
            let textToCopy;
            
            if (content) {
                textToCopy = content;
            } else if (elementId) {
                const element = document.getElementById(elementId);
                textToCopy = element.textContent;
            } else {
                throw new Error('No content to copy');
            }

            await navigator.clipboard.writeText(textToCopy);
            this.showToast('Content copied to clipboard!', 'success');
        } catch (error) {
            console.error('Error copying to clipboard:', error);
            this.showToast('Failed to copy content', 'error');
        }
    }

    async downloadContent(elementId, content = null) {
        try {
            let textToDownload;
            
            if (content) {
                textToDownload = content;
            } else if (elementId) {
                const element = document.getElementById(elementId);
                textToDownload = element.textContent;
            } else {
                throw new Error('No content to download');
            }

            if (!this.currentRewrite) {
                this.showToast('No content to download', 'error');
                return;
            }

            // Create download data
            const downloadData = {
                rewrite_data: this.currentRewrite,
                format: 'txt'
            };

            const response = await fetch('/api/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(downloadData)
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    // Trigger download
                    const link = document.createElement('a');
                    link.href = `/api/download/${result.file_path.split('/').pop()}`;
                    link.download = `rewrite_${this.currentRewrite.metadata.tone}_${new Date().toISOString().slice(0, 10)}.txt`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    this.showToast('Content downloaded successfully!', 'success');
                } else {
                    this.showToast(result.error || 'Failed to download content', 'error');
                }
            } else {
                this.showToast('Failed to download content', 'error');
            }

        } catch (error) {
            console.error('Error downloading content:', error);
            this.showToast('Failed to download content', 'error');
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        const btn = document.getElementById('rewriteBtn');
        const btnText = document.getElementById('btnText');
        const spinner = document.getElementById('loadingSpinner');

        if (loading) {
            btn.disabled = true;
            btnText.textContent = 'Rewriting...';
            spinner.classList.remove('hidden');
        } else {
            btn.disabled = false;
            btnText.textContent = 'Rewrite Content';
            spinner.classList.add('hidden');
        }
    }

    hideResults() {
        document.getElementById('resultsSection').classList.add('hidden');
    }

    showChatbot() {
        this.showToast('Chatbot feature coming soon! For now, use the examples or try different tones.', 'info');
        
        // Add some visual feedback
        const chatbotBtn = document.getElementById('chatbotBtn');
        if (chatbotBtn) {
            chatbotBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                chatbotBtn.style.transform = 'scale(1)';
            }, 150);
        }
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toastMessage');
        
        // Update message and styling
        toastMessage.textContent = message;
        
        // Remove existing type classes
        toast.classList.remove('bg-green-500', 'bg-red-500', 'bg-blue-500', 'bg-yellow-500');
        
        // Add appropriate type class
        switch (type) {
            case 'success':
                toast.classList.add('bg-green-500');
                break;
            case 'error':
                toast.classList.add('bg-red-500');
                break;
            case 'warning':
                toast.classList.add('bg-yellow-500');
                break;
            default:
                toast.classList.add('bg-blue-500');
        }
        
        // Show toast
        toast.classList.remove('translate-x-full');
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.classList.add('translate-x-full');
        }, 3000);
    }
}

// Global function for example loading
function loadExample(type) {
    if (window.articleRewriterApp) {
        window.articleRewriterApp.loadExample(type);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.articleRewriterApp = new ArticleRewriterApp();
});

// Add some nice effects
document.addEventListener('DOMContentLoaded', () => {
    // Add typing effect to placeholder
    const contentTextarea = document.getElementById('content');
    const placeholders = [
        "Paste your article, blog post, or any text content here...",
        "Enter your content to rewrite in a different tone...",
        "Transform your writing style with AI...",
        "Make your content shine with a new tone..."
    ];
    
    let placeholderIndex = 0;
    setInterval(() => {
        if (document.activeElement !== contentTextarea && !contentTextarea.value) {
            contentTextarea.placeholder = placeholders[placeholderIndex];
            placeholderIndex = (placeholderIndex + 1) % placeholders.length;
        }
    }, 3000);
});
