// StoryWriterAgent - Main JavaScript Application

class StoryWriterApp {
    constructor() {
        this.currentStory = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupExampleCards();
        this.setupKeyboardShortcuts();
        this.setupAnimations();
        this.setupAutoSave();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('storyForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Action buttons
        const saveBtn = document.getElementById('saveBtn');
        const favoriteBtn = document.getElementById('favoriteBtn');
        const downloadBtn = document.getElementById('downloadBtn');
        const newStoryBtn = document.getElementById('newStoryBtn');

        if (saveBtn) saveBtn.addEventListener('click', () => this.saveStory());
        if (favoriteBtn) favoriteBtn.addEventListener('click', () => this.toggleFavorite());
        if (downloadBtn) downloadBtn.addEventListener('click', () => this.downloadStory());
        if (newStoryBtn) newStoryBtn.addEventListener('click', () => this.newStory());
    }

    setupExampleCards() {
        const exampleCards = document.querySelectorAll('.example-card');
        exampleCards.forEach(card => {
            card.addEventListener('click', () => {
                const prompt = card.dataset.prompt;
                if (prompt) {
                    document.getElementById('prompt').value = prompt;
                    this.showToast('Example loaded! You can modify the prompt or generate as is.', 'success');
                }
            });
        });
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const storyData = {
            prompt: formData.get('prompt'),
            genre: formData.get('genre'),
            tone: formData.get('tone'),
            length: formData.get('length'),
            language: formData.get('language')
        };

        // Validate input
        if (!storyData.prompt.trim()) {
            this.showToast('Please enter a story prompt!', 'error');
            return;
        }

        await this.generateStory(storyData);
    }

    async generateStory(storyData) {
        const generateBtn = document.getElementById('generateBtn');
        const loading = document.getElementById('loading');
        const storyDisplay = document.getElementById('storyDisplay');

        try {
            // Show loading state with enhanced animation
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
            generateBtn.classList.add('generating');
            loading.style.display = 'block';
            storyDisplay.style.display = 'none';

            // Add progress simulation
            this.simulateProgress();

            // Make API request
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(storyData)
            });

            const result = await response.json();

            if (result.success) {
                this.currentStory = result.story;
                this.displayStory(result.story);
                this.showToast('Story generated successfully!', 'success');
            } else {
                throw new Error(result.error || 'Failed to generate story');
            }

        } catch (error) {
            console.error('Error generating story:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        } finally {
            // Reset UI
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Story';
            generateBtn.classList.remove('generating');
            loading.style.display = 'none';
        }
    }

    simulateProgress() {
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        progressBar.innerHTML = '<div class="progress-fill"></div>';
        
        const loading = document.getElementById('loading');
        loading.appendChild(progressBar);
        
        const progressFill = progressBar.querySelector('.progress-fill');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
        }, 200);
        
        // Clear interval when story is generated
        setTimeout(() => {
            clearInterval(interval);
            progressFill.style.width = '100%';
            setTimeout(() => {
                if (progressBar.parentNode) {
                    progressBar.parentNode.removeChild(progressBar);
                }
            }, 500);
        }, 3000);
    }

    displayStory(story) {
        const storyDisplay = document.getElementById('storyDisplay');
        const storyTitle = document.getElementById('storyTitle');
        const storyContent = document.getElementById('storyContent');
        const storyGenre = document.getElementById('storyGenre');
        const storyTone = document.getElementById('storyTone');
        const storyLength = document.getElementById('storyLength');
        const storyLanguage = document.getElementById('storyLanguage');

        // Update story metadata immediately
        storyTitle.textContent = story.title;
        storyGenre.textContent = story.genre;
        storyTone.textContent = story.tone;
        storyLength.textContent = story.length;
        storyLanguage.textContent = story.language;

        // Show story display
        storyDisplay.style.display = 'block';
        storyDisplay.scrollIntoView({ behavior: 'smooth' });

        // Start typewriter effect for story content
        this.typewriterEffect(storyContent, story.content);
    }

    typewriterEffect(element, text, speed = 30) {
        element.textContent = '';
        element.style.borderRight = '2px solid #6366f1';
        element.style.animation = 'blink 1s infinite';
        element.classList.add('typing');
        
        let i = 0;
        let currentWord = '';
        let isTyping = true;
        
        const timer = setInterval(() => {
            if (i < text.length && isTyping) {
                const char = text.charAt(i);
                element.textContent += char;
                i++;
                
                // Add word highlighting effect
                if (char === ' ' || char === '\n') {
                    this.highlightLastWord(element);
                }
                
                // Scroll to keep the typing visible
                element.scrollTop = element.scrollHeight;
                
                // Add sound effect simulation (visual feedback)
                if (Math.random() < 0.1) {
                    element.style.transform = 'scale(1.001)';
                    setTimeout(() => {
                        element.style.transform = 'scale(1)';
                    }, 50);
                }
            } else {
                clearInterval(timer);
                element.style.borderRight = 'none';
                element.style.animation = 'none';
                element.classList.remove('typing');
                
                // Add completion effect
                this.addCompletionEffect(element);
            }
        }, speed);
        
        // Add pause/resume functionality
        element.addEventListener('click', () => {
            isTyping = !isTyping;
            if (!isTyping) {
                element.style.borderRight = 'none';
                element.style.animation = 'none';
            } else {
                element.style.borderRight = '2px solid #6366f1';
                element.style.animation = 'blink 1s infinite';
            }
        });
    }

    highlightLastWord(element) {
        const text = element.textContent;
        const words = text.split(' ');
        if (words.length > 1) {
            const lastWord = words[words.length - 2]; // Second to last word
            const highlightedText = text.replace(
                new RegExp(`\\b${lastWord}\\b`, 'g'),
                `<span style="background: rgba(99, 102, 241, 0.2); padding: 2px 4px; border-radius: 3px;">${lastWord}</span>`
            );
            element.innerHTML = highlightedText;
        }
    }

    addCompletionEffect(element) {
        // Add completion animation
        element.style.background = 'linear-gradient(45deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1))';
        element.style.transform = 'scale(1.02)';
        element.style.transition = 'all 0.5s ease';
        
        // Add sparkle effect
        this.addSparkleEffect(element);
        
        setTimeout(() => {
            element.style.background = '';
            element.style.transform = 'scale(1)';
        }, 2000);
    }

    addSparkleEffect(element) {
        const sparkle = document.createElement('div');
        sparkle.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            width: 20px;
            height: 20px;
            background: linear-gradient(45deg, #6366f1, #8b5cf6);
            border-radius: 50%;
            animation: pulse 0.5s ease-out;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.appendChild(sparkle);
        
        setTimeout(() => {
            if (sparkle.parentNode) {
                sparkle.parentNode.removeChild(sparkle);
            }
        }, 1000);
    }

    async saveStory() {
        if (!this.currentStory) {
            this.showToast('No story to save!', 'error');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('story_id', this.currentStory.id);
            formData.append('format', 'both');

            const response = await fetch('/api/save', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.showToast('Story saved successfully!', 'success');
            } else {
                throw new Error(result.error || 'Failed to save story');
            }

        } catch (error) {
            console.error('Error saving story:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    async toggleFavorite() {
        if (!this.currentStory) {
            this.showToast('No story to favorite!', 'error');
            return;
        }

        try {
            const response = await fetch(`/api/favorites/${this.currentStory.id}`, {
                method: 'POST'
            });

            const result = await response.json();

            if (result.success) {
                const favoriteBtn = document.getElementById('favoriteBtn');
                const isFavorited = favoriteBtn.classList.contains('favorited');
                
                if (isFavorited) {
                    favoriteBtn.classList.remove('favorited');
                    favoriteBtn.innerHTML = '<i class="fas fa-heart"></i> Add to Favorites';
                    this.showToast('Removed from favorites', 'success');
                } else {
                    favoriteBtn.classList.add('favorited');
                    favoriteBtn.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
                    this.showToast('Added to favorites', 'success');
                }
            } else {
                throw new Error(result.error || 'Failed to toggle favorite');
            }

        } catch (error) {
            console.error('Error toggling favorite:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    async downloadStory() {
        if (!this.currentStory) {
            this.showToast('No story to download!', 'error');
            return;
        }

        try {
            // Create download link
            const content = `Title: ${this.currentStory.title}\n` +
                          `Genre: ${this.currentStory.genre}\n` +
                          `Tone: ${this.currentStory.tone}\n` +
                          `Length: ${this.currentStory.length}\n` +
                          `Language: ${this.currentStory.language}\n` +
                          `Created: ${this.currentStory.created_at}\n` +
                          `Word Count: ${this.currentStory.word_count}\n` +
                          `-`.repeat(50) + `\n\n` +
                          this.currentStory.content;

            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${this.currentStory.title.replace(/[^a-zA-Z0-9]/g, '_')}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.showToast('Story downloaded!', 'success');

        } catch (error) {
            console.error('Error downloading story:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    newStory() {
        // Reset form
        document.getElementById('storyForm').reset();
        
        // Hide story display
        const storyDisplay = document.getElementById('storyDisplay');
        storyDisplay.style.display = 'none';
        
        // Clear current story
        this.currentStory = null;
        
        // Focus on prompt input
        document.getElementById('prompt').focus();
        
        this.showToast('Ready for a new story!', 'success');
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        if (!toast) return;

        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.add('show');

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to generate story
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                const form = document.getElementById('storyForm');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
            
            // Escape to clear form
            if (e.key === 'Escape') {
                this.clearForm();
            }
            
            // Ctrl/Cmd + S to save story
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                this.saveStory();
            }
            
            // Ctrl/Cmd + N for new story
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                this.newStory();
            }
        });
    }

    setupAnimations() {
        // Add entrance animations to elements
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease-out';
                }
            });
        });

        // Observe all form groups and cards
        document.querySelectorAll('.form-group, .example-card, .story-card').forEach(el => {
            observer.observe(el);
        });
    }

    setupAutoSave() {
        // Auto-save form data to localStorage
        const form = document.getElementById('storyForm');
        if (form) {
            // Load saved data
            this.loadFormData();
            
            // Save on input change
            form.addEventListener('input', () => {
                this.saveFormData();
            });
        }
    }

    saveFormData() {
        const form = document.getElementById('storyForm');
        if (!form) return;

        const formData = new FormData(form);
        const data = {
            prompt: formData.get('prompt') || '',
            genre: formData.get('genre') || 'fantasy',
            tone: formData.get('tone') || 'serious',
            length: formData.get('length') || 'medium',
            language: formData.get('language') || 'english'
        };

        localStorage.setItem('storyWriterFormData', JSON.stringify(data));
    }

    loadFormData() {
        const savedData = localStorage.getItem('storyWriterFormData');
        if (!savedData) return;

        try {
            const data = JSON.parse(savedData);
            
            // Populate form fields
            const promptField = document.getElementById('prompt');
            const genreField = document.getElementById('genre');
            const toneField = document.getElementById('tone');
            const lengthField = document.getElementById('length');
            const languageField = document.getElementById('language');

            if (promptField) promptField.value = data.prompt || '';
            if (genreField) genreField.value = data.genre || 'fantasy';
            if (toneField) toneField.value = data.tone || 'serious';
            if (lengthField) lengthField.value = data.length || 'medium';
            if (languageField) languageField.value = data.language || 'english';
        } catch (e) {
            console.warn('Failed to load saved form data:', e);
        }
    }

    clearForm() {
        const form = document.getElementById('storyForm');
        if (form) {
            form.reset();
            localStorage.removeItem('storyWriterFormData');
            this.showToast('Form cleared!', 'success');
        }
    }

    // Enhanced example card functionality
    setupExampleCards() {
        const exampleCards = document.querySelectorAll('.example-card');
        exampleCards.forEach(card => {
            card.addEventListener('click', () => {
                const prompt = card.dataset.prompt;
                if (prompt) {
                    document.getElementById('prompt').value = prompt;
                    this.showToast('Example loaded! You can modify the prompt or generate as is.', 'success');
                    
                    // Add visual feedback
                    card.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        card.style.transform = 'scale(1)';
                    }, 150);
                }
            });
            
            // Add hover effects
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    // Add word count and character count
    updateWordCount() {
        const promptField = document.getElementById('prompt');
        if (!promptField) return;

        const text = promptField.value;
        const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        const charCount = text.length;

        // Create or update word count display
        let wordCountDisplay = document.getElementById('wordCountDisplay');
        if (!wordCountDisplay) {
            wordCountDisplay = document.createElement('div');
            wordCountDisplay.id = 'wordCountDisplay';
            wordCountDisplay.style.cssText = `
                position: absolute;
                bottom: 10px;
                right: 10px;
                font-size: 0.8rem;
                color: var(--text-muted);
                background: rgba(255, 255, 255, 0.9);
                padding: 4px 8px;
                border-radius: 4px;
                pointer-events: none;
            `;
            promptField.parentElement.style.position = 'relative';
            promptField.parentElement.appendChild(wordCountDisplay);
        }

        wordCountDisplay.textContent = `${wordCount} words, ${charCount} characters`;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StoryWriterApp();
});

// Utility functions
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('Text copied to clipboard');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    }
}

// Auto-resize textarea
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Add auto-resize to prompt textarea
document.addEventListener('DOMContentLoaded', () => {
    const promptTextarea = document.getElementById('prompt');
    if (promptTextarea) {
        promptTextarea.addEventListener('input', () => {
            autoResizeTextarea(promptTextarea);
        });
    }
});
