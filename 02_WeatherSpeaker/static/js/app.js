// Weather Speaker Agent - Frontend JavaScript
class WeatherApp {
    constructor() {
        document.getElementById('loadingOverlay').classList.remove('active');
        this.currentCity = '';
        this.isLoading = false;
        this.init();
        // Optionally, auto-fetch if ?city= is present in the URL
        const params = new URLSearchParams(window.location.search);
        const city = params.get('city');
        if (city) {
            document.getElementById('cityInput').value = city;
            this.getWeather(city);
        }
    }

    init() {
        this.bindEvents();
        this.setupAnimations();
    }

    bindEvents() {
        // Form submission
        const form = document.getElementById('weatherForm');
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

        // Get tips button
        const getTipsBtn = document.getElementById('getTipsBtn');
        getTipsBtn.addEventListener('click', () => this.getWeatherTips());

        // Enter key on input
        const cityInput = document.getElementById('cityInput');
        cityInput.addEventListener('keypress', (e) => {
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
        const cityInput = document.getElementById('cityInput');
        const city = cityInput.value.trim();
        
        if (!city) {
            this.showError('Please enter a city name');
            return;
        }

        this.currentCity = city;
        this.getWeather(city);
    }

    async getWeather(city) {
        this.setLoading(true);
        this.hideAllDisplays();
        this.showLoadingOverlay(true);

        try {
            const voiceEnabled = document.getElementById('voiceToggle').checked;
            
            const response = await fetch('/api/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    city: city,
                    include_voice: voiceEnabled
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // If no weather data and not success, show no results
            if (!data.success && data.error && data.error.toLowerCase().includes('not found')) {
                this.showNoResults();
            } else if (data.success) {
                this.displayWeather(data);
                this.toggleVoiceControls();
            } else {
                this.showError(data.error || 'Failed to get weather data');
            }
        } catch (error) {
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.setLoading(false);
            this.showLoadingOverlay(false);
        }
    }

    displayWeather(data) {
        try {
            this.hideAllDisplays();
            const weatherData = data.weather_data;
            if (!weatherData) {
                this.showNoResults();
                return;
            }

            const current = weatherData.current;
            const forecast = weatherData.forecast;

            if (!current || !forecast) {
                this.showNoResults();
                return;
            }

            // Update weather card
            document.getElementById('cityName').textContent = `${weatherData.city}${weatherData.country ? `, ${weatherData.country}` : ''}`;
            document.getElementById('temperature').textContent = Math.round(current.temperature || 0);
            document.getElementById('feelsLike').textContent = Math.round(current.feels_like || 0);
            document.getElementById('humidity').textContent = `${current.humidity || 0}%`;
            document.getElementById('windSpeed').textContent = `${current.wind_speed || 0} km/h`;
            document.getElementById('todayMax').textContent = `${Math.round(forecast.today_max || 0)}°C`;
            document.getElementById('todayMin').textContent = `${Math.round(forecast.today_min || 0)}°C`;

            // Update weather description and icon
            const weatherDesc = this.getWeatherDescription(current.weather_code);
            const weatherIcon = this.getWeatherIcon(current.weather_code);
            document.getElementById('weatherDesc').textContent = weatherDesc;
            document.getElementById('weatherIcon').textContent = weatherIcon;

            // Update AI response
            const aiText = data.ai_response || 'Weather information available.';
            document.getElementById('aiText').textContent = aiText;

            // Show displays
            document.getElementById('weatherDisplay').classList.remove('hidden');
            
            // Scroll to weather display
            setTimeout(() => {
                document.getElementById('weatherDisplay').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 100);
        } catch (error) {
            this.showError('Error displaying weather data');
        }
    }

    async getWeatherTips() {
        if (!this.currentCity) return;

        const getTipsBtn = document.getElementById('getTipsBtn');
        const originalText = getTipsBtn.textContent;
        getTipsBtn.textContent = 'Loading...';
        getTipsBtn.disabled = true;

        try {
            const response = await fetch('/api/weather/tips', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    city: this.currentCity
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.tips) {
                document.getElementById('tipsText').textContent = data.tips;
            } else {
                document.getElementById('tipsText').textContent = 'No tips available at the moment.';
            }
        } catch (error) {
            document.getElementById('tipsText').textContent = 'Unable to load weather tips.';
        } finally {
            getTipsBtn.textContent = originalText;
            getTipsBtn.disabled = false;
        }
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
            btnText.textContent = 'Getting Weather...';
            loadingSpinner.classList.remove('hidden');
        } else {
            submitBtn.disabled = false;
            btnText.textContent = 'Get Weather';
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
        document.getElementById('weatherDisplay').classList.add('hidden');
        document.getElementById('errorDisplay').classList.add('hidden');
        document.getElementById('noResultsDisplay').classList.add('hidden');
        this.showLoadingOverlay(false);
    }

    getWeatherDescription(weatherCode) {
        const descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        };
        
        return descriptions[weatherCode] || "Unknown weather condition";
    }

    getWeatherIcon(weatherCode) {
        if (weatherCode in [0, 1]) return "☀️";
        if (weatherCode in [2, 3]) return "☁️";
        if (weatherCode in [45, 48]) return "🌫️";
        if (weatherCode in [51, 53, 55, 56, 57]) return "🌦️";
        if (weatherCode in [61, 63, 65, 66, 67, 80, 81, 82]) return "🌧️";
        if (weatherCode in [71, 73, 75, 77, 85, 86]) return "❄️";
        if (weatherCode in [95, 96, 99]) return "⛈️";
        return "🌤️";
    }
}

// Initialize the app when DOM is loaded
// Also ensure loading overlay is hidden on page load
// (double safety in case of hot reload or script errors)
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('loadingOverlay').classList.remove('active');
    new WeatherApp();
});

// Add some nice effects
document.addEventListener('DOMContentLoaded', () => {
    // Add typing effect to placeholder
    const cityInput = document.getElementById('cityInput');
    const placeholders = [
        "e.g., New York, London, Tokyo...",
        "e.g., Paris, Sydney, Dubai...",
        "e.g., Berlin, Mumbai, Rio...",
        "e.g., New York, London, Tokyo..."
    ];
    
    let placeholderIndex = 0;
    setInterval(() => {
        if (document.activeElement !== cityInput) {
            cityInput.placeholder = placeholders[placeholderIndex];
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