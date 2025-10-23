// frontend/app.js

document.addEventListener('DOMContentLoaded', () => {
    const currentDateElement = document.getElementById('current-date');
    const quoteElement = document.getElementById('quote');
    const messageElement = document.getElementById('message');
    const audioPlayer = document.getElementById('audio-player');
    const newQuoteBtn = document.getElementById('new-quote-btn');
    const downloadAudioBtn = document.getElementById('download-audio-btn');
    const copyTextBtn = document.getElementById('copy-text-btn');
    const currentYearElement = document.getElementById('current-year');
    const loadingOverlay = document.getElementById('loading-overlay');
    const btnSpinner = document.getElementById('btn-spinner');
    const motivationBackgroundImage = document.getElementById('motivation-background-image');
    const quoteTextOverlay = document.getElementById('quote-text-overlay');
    const errorDisplay = document.getElementById('error-display');
    const errorMessage = document.getElementById('error-message');
    const closeErrorBtn = document.getElementById('close-error');

    // Navbar and Popup elements
    const aboutBtnNavbar = document.getElementById('about-btn-navbar');
    const welcomePopup = document.getElementById('welcome-popup');
    const welcomeYesBtn = document.getElementById('welcome-yes-btn');
    const welcomeNoBtn = document.getElementById('welcome-no-btn');
    const aboutPopup = document.getElementById('about-popup');
    const closeAboutPopup = document.getElementById('close-about-popup');
    const aboutContent = document.getElementById('about-content');
    const languageSelect = document.getElementById('language-select');

    // Helper function for showing tooltips
    const showTooltip = (btn, message) => {
        const oldTooltip = btn.parentElement.querySelector('.btn-tooltip');
        if (oldTooltip) oldTooltip.remove();

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
    };

    // Helper function for gold glow effect
    const goldGlowEffect = (btn) => {
        btn.classList.add('ring-4', 'ring-gold', 'ring-opacity-60');
        setTimeout(() => {
            btn.classList.remove('ring-4', 'ring-gold', 'ring-opacity-60');
        }, 400);
    };

    // Set current date and year
    const today = new Date();
    currentDateElement.textContent = today.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    currentYearElement.textContent = today.getFullYear();

    // Function to get a random image URL
    const getRandomImageUrl = () => {
        const width = 800;
        const height = 600;
        const cacheBuster = `t=${Date.now()}`;
        return `https://picsum.photos/${width}/${height}?${cacheBuster}`;
    };

    // Function to show loading overlay
    const showLoading = () => {
        loadingOverlay.classList.remove('hidden');
        btnSpinner.classList.remove('hidden');
        newQuoteBtn.querySelector('span').classList.add('hidden');
    };

    // Function to hide loading overlay
    const hideLoading = () => {
        loadingOverlay.classList.add('hidden');
        btnSpinner.classList.add('hidden');
        newQuoteBtn.querySelector('span').classList.remove('hidden');
    };

    // Function to show error message
    const showError = (message) => {
        errorMessage.textContent = message;
        errorDisplay.classList.remove('hidden');
    };

    // Function to hide error message
    const hideError = () => {
        errorDisplay.classList.add('hidden');
    };

    // Function to show welcome popup
    const showWelcomePopup = () => {
        welcomePopup.classList.remove('hidden');
    };

    // Function to hide welcome popup
    const hideWelcomePopup = () => {
        welcomePopup.classList.add('hidden');
    };

    // Function to show about popup and load README content
    const showAboutPopup = async () => {
        aboutPopup.classList.remove('hidden');
        // Fetch README content from backend
        try {
            const response = await fetch('/api/about');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const readmeContent = await response.text();
            aboutContent.innerHTML = markdownit().render(readmeContent); // Assuming markdown-it is loaded
        } catch (error) {
            console.error('Error fetching README content:', error);
            aboutContent.innerHTML = '<p class="text-red-400">Failed to load About content. Please try again.</p>';
        }
    };

    // Function to hide about popup
    const hideAboutPopup = () => {
        aboutPopup.classList.add('hidden');
    };

    const fetchMotivation = async (name = null) => {
        showLoading(); // Show loading overlay
        hideError(); // Hide any previous errors

        quoteElement.textContent = '';
        messageElement.textContent = '';
        audioPlayer.classList.add('hidden');
        downloadAudioBtn.classList.add('hidden');
        copyTextBtn.classList.add('hidden');

        try {
            const selectedLanguage = languageSelect.value;
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ language: selectedLanguage, name: name }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            quoteElement.textContent = `"${data.quote}"`;
            messageElement.textContent = data.message;
            audioPlayer.src = data.audio_url;
            audioPlayer.load();
            audioPlayer.classList.remove('hidden');
            downloadAudioBtn.classList.remove('hidden');
            copyTextBtn.classList.remove('hidden');

            // Set random background image and ensure overlay is visible
            motivationBackgroundImage.src = getRandomImageUrl();
            motivationBackgroundImage.classList.remove('opacity-0');
            quoteTextOverlay.style.background = 'rgba(24,24,27,0.25)'; // Dark overlay for readability

        } catch (error) {
            console.error('Error fetching motivation:', error);
            showError(error.message || 'Failed to load motivation. Please try again.');
            quoteElement.textContent = ''; // Clear quote/message on error
            messageElement.textContent = '';
            motivationBackgroundImage.classList.add('opacity-0'); // Hide image on error
            quoteTextOverlay.style.background = 'none'; // Remove overlay on error
        } finally {
            hideLoading(); // Hide loading overlay regardless of success or failure
        }
    };

    // Event Listeners
    aboutBtnNavbar.addEventListener('click', showAboutPopup);
    closeAboutPopup.addEventListener('click', hideAboutPopup);

    welcomeYesBtn.addEventListener('click', () => {
        hideWelcomePopup();
        // const userName = prompt("Enter your name (optional, for a personalized message):");
        fetchMotivation(null);
    });

    welcomeNoBtn.addEventListener('click', () => {
        hideWelcomePopup();
    });

    newQuoteBtn.addEventListener('click', () => {
        // const userName = prompt("Enter your name (optional, for a personalized message):");
        fetchMotivation(null);
    });

    downloadAudioBtn.addEventListener('click', () => {
        const audioLink = audioPlayer.src;
        if (audioLink) {
            const a = document.createElement('a');
            a.href = audioLink;
            a.download = 'daily_motivation.mp3';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            goldGlowEffect(downloadAudioBtn);
            showTooltip(downloadAudioBtn, 'Audio Downloaded!');
        } else {
            showTooltip(downloadAudioBtn, 'No audio to download!');
        }
    });

    copyTextBtn.addEventListener('click', () => {
        const textToCopy = `"${quoteElement.textContent}"\n\n${messageElement.textContent}`;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                goldGlowEffect(copyTextBtn);
                showTooltip(copyTextBtn, 'Text Copied!');
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                showTooltip(copyTextBtn, 'Failed to Copy!');
            });
    });

    closeErrorBtn.addEventListener('click', hideError);

    // Initial setup
    showWelcomePopup();
});
