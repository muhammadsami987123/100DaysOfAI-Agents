// Location Info Agent - Frontend JavaScript
class LocationApp {
    constructor() {
        document.getElementById('loadingOverlay').classList.remove('active');
        this.currentPlace = '';
        this.isLoading = false;
        this.init();
        // Optionally, auto-fetch if ?place= is present in the URL
        const params = new URLSearchParams(window.location.search);
        const place = params.get('place');
        if (place) {
            document.getElementById('placeInput').value = place;
            this.exploreLocation(place);
        }
    }

    init() {
        this.bindEvents();
        this.setupAnimations();
    }

    bindEvents() {
        // Form submission
        const form = document.getElementById('locationForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent page reload and URL update
            this.handleSubmit(e);
        });

        // Voice toggle
        const voiceToggle = document.getElementById('voiceToggle');
        voiceToggle.addEventListener('change', () => this.toggleVoiceControls());

        // Stop voice button
        const stopVoiceBtn = document.getElementById('stopVoiceBtn');
        stopVoiceBtn.addEventListener('click', () => this.stopVoice());

        // Enter key on input
        const placeInput = document.getElementById('placeInput');
        placeInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.handleSubmit(e);
            }
        });
    }

    setupAnimations() {
        // Add entrance animations
        const elements = document.querySelectorAll('.animate-fade-in, .animate-slide-up');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        });

        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            observer.observe(el);
        });
    }

    handleSubmit(e) {
        const placeInput = document.getElementById('placeInput');
        const place = placeInput.value.trim();
        
        if (!place) {
            this.showError('Please enter a location name');
            return;
        }

        this.currentPlace = place;
        this.exploreLocation(place);
    }

    async exploreLocation(place) {
        this.setLoading(true);
        this.hideAllDisplays();
        this.showLoadingOverlay(true);

        try {
            const voiceEnabled = document.getElementById('voiceToggle').checked;
            
            const response = await fetch('/api/explore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    place: place,
                    include_voice: voiceEnabled
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.ai_response || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (!data.success && data.error && data.error.toLowerCase().includes('not found')) {
                this.showNoResults();
            } else if (data.success) {
                this.displayLocation(data);
                this.toggleVoiceControls();
            } else {
                this.showError(data.ai_response || data.error || 'Failed to get location information');
            }
        } catch (error) {
            this.showError(error.message || 'Network error. Please check your connection and try again.');
        } finally {
            this.setLoading(false);
            this.showLoadingOverlay(false);
        }
    }

    displayLocation(data) {
        try {
            this.hideAllDisplays();
            const locationData = data.location_data;
            if (!locationData) {
                this.showNoResults();
                return;
            }

            // Update location name and AI response
            document.getElementById('locationName').textContent = locationData.name || 'Unknown Location';
            document.getElementById('aiResponseText').innerHTML = data.ai_response ? this.formatTextAsHtml(data.ai_response) : 'No detailed information available.';

            // Update map embed
            const mapContainer = document.getElementById('mapContainer');
            const googleMap = document.getElementById('googleMap');
            if (data.map_embed_url) {
                googleMap.src = data.map_embed_url;
                mapContainer.classList.remove('hidden');
            } else {
                mapContainer.classList.add('hidden');
            }

            // Update image gallery
            const imageGallery = document.getElementById('imageGallery');
            imageGallery.innerHTML = ''; // Clear previous images
            if (data.image_urls && data.image_urls.length > 0) {
                data.image_urls.forEach(url => {
                    const imgDiv = document.createElement('div');
                    imgDiv.className = 'rounded-lg overflow-hidden shadow-md transition-transform duration-300 hover:scale-105';
                    imgDiv.innerHTML = `<img src="${url}" alt="Location image" class="w-full h-48 object-cover">`;
                    imageGallery.appendChild(imgDiv);
                });
                imageGallery.classList.remove('hidden');
            } else {
                imageGallery.classList.add('hidden');
            }

            // Show displays
            document.getElementById('locationDisplay').classList.remove('hidden');
            
            // Scroll to location display
            setTimeout(() => {
                document.getElementById('locationDisplay').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 100);
        } catch (error) {
            this.showError('Error displaying location data');
        }
    }

    formatTextAsHtml(text) {
        // Convert markdown-like headings and lists to HTML for better display within the prose class
        let formattedText = text.replace(/^### (.*)$/gm, '<h3>$1</h3>');
        formattedText = formattedText.replace(/^## (.*)$/gm, '<h2>$1</h2>');
        formattedText = formattedText.replace(/^# (.*)$/gm, '<h1>$1</h1>');
        formattedText = formattedText.replace(/^\* (.*)$/gm, '<li>$1</li>');
        formattedText = formattedText.replace(/\n\n(?=\*)/g, '<ul>'); // Start unordered list
        formattedText = formattedText.replace(/(\s*<li>.*<\/li>)+\s*\n\n/g, '</ul><br><br>'); // End unordered list
        // Basic bolding
        formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Replace remaining newlines with <br> for general paragraphs
        formattedText = formattedText.replace(/\n/g, '<br>');
        return formattedText;
    }

    async stopVoice() {
        try {
            const response = await fetch('/api/voice/stop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const stopVoiceBtn = document.getElementById('stopVoiceBtn');
                stopVoiceBtn.classList.add('hidden');
            }
        } catch (error) {
            // Ignore
        }
    }

    toggleVoiceControls() {
        const voiceEnabled = document.getElementById('voiceToggle').checked;
        const stopVoiceBtn = document.getElementById('stopVoiceBtn');
        
        if (voiceEnabled) {
            stopVoiceBtn.classList.remove('hidden');
        } else {
            stopVoiceBtn.classList.add('hidden');
        }
    }

    setLoading(loading) {
        this.isLoading = loading;
        const submitBtn = document.getElementById('submitBtn');
        const btnText = document.getElementById('btnText');
        const loadingSpinner = document.getElementById('loadingSpinner');

        if (loading) {
            submitBtn.disabled = true;
            btnText.textContent = 'Exploring...';
            loadingSpinner.classList.remove('hidden');
        } else {
            submitBtn.disabled = false;
            btnText.textContent = 'Explore';
            loadingSpinner.classList.add('hidden');
        }
    }

    showLoadingOverlay(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }

    showError(message) {
        this.hideAllDisplays();
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorDisplay').classList.remove('hidden');
        // Hide after 5 seconds
        setTimeout(() => {
            document.getElementById('errorDisplay').classList.add('hidden');
        }, 5000);
    }

    showNoResults() {
        this.hideAllDisplays();
        document.getElementById('noResultsDisplay').classList.remove('hidden');
    }

    hideAllDisplays() {
        document.getElementById('locationDisplay').classList.add('hidden');
        document.getElementById('errorDisplay').classList.add('hidden');
        document.getElementById('noResultsDisplay').classList.add('hidden');
        this.showLoadingOverlay(false);
    }
}

// Initialize the app when DOM is loaded
// Also ensure loading overlay is hidden on page load
// (double safety in case of hot reload or script errors)
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('loadingOverlay').classList.remove('active');
    new LocationApp();
});

// Add some nice effects
document.addEventListener('DOMContentLoaded', () => {
    // Add typing effect to placeholder
    const placeInput = document.getElementById('placeInput');
    const placeholders = [
        "e.g., Paris, Great Wall, Japan...",
        "e.g., Rome, Statue of Liberty, Brazil...",
        "e.g., London, Eiffel Tower, Egypt...",
        "e.g., New York, Mount Everest, Canada..."
    ];
    
    let placeholderIndex = 0;
    setInterval(() => {
        if (document.activeElement !== placeInput) {
            placeInput.placeholder = placeholders[placeholderIndex];
            placeholderIndex = (placeholderIndex + 1) % placeholders.length;
        }
    }, 3000);

    // Add particle effect to background
    createParticles();
});

function createParticles() {
    const body = document.body;
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: fixed;
            width: 2px;
            height: 2px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            pointer-events: none;
            animation: float ${3 + Math.random() * 4}s linear infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation-delay: ${Math.random() * 2}s;
        `;
        body.appendChild(particle);
    }
}

// Add CSS for particles
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    .particle {
        z-index: -1;
    }
`;
document.head.appendChild(style);
