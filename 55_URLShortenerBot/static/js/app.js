document.addEventListener('DOMContentLoaded', () => {
    const shortenForm = document.getElementById('shortenForm');
    const longUrlInput = document.getElementById('longUrl');
    const aliasInput = document.getElementById('alias');
    const shortenButton = shortenForm.querySelector('button[type="submit"]');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const copyToClipboardCheckbox = document.getElementById('copyToClipboard');
    const generateQrCheckbox = document.getElementById('generateQr');
    const shortLinkOutput = document.getElementById('shortLinkOutput');
    const qrCodeImage = document.getElementById('qrCodeImage');
    const messageDiv = document.getElementById('message');
    const themeToggle = document.getElementById('themeToggle');
    const langSelector = document.getElementById('langSelector');
    const resultSection = document.getElementById('resultSection');

    // Theme Toggle
    themeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode', themeToggle.checked);
        localStorage.setItem('darkMode', themeToggle.checked);
    });

    // Load saved theme preference
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        themeToggle.checked = true;
    }

    // Language Selector (mocked for now)
    langSelector.addEventListener('change', () => {
        const selectedLang = langSelector.value;
        console.log(`Language switched to: ${selectedLang}`);
        // In a real application, you would load translations here
        alert(`Language feature mocked. Selected: ${selectedLang}`);
    });

    // Click to copy short link
    shortLinkOutput.addEventListener('click', () => {
        if (shortLinkOutput.textContent) {
            navigator.clipboard.writeText(shortLinkOutput.textContent)
                .then(() => showMessage('Short link copied to clipboard!', 'success'))
                .catch(err => console.error('Failed to copy text:', err));
        }
    });

    shortenForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        shortenButton.disabled = true; // Disable button during submission
        shortenButton.textContent = 'Generating...'; // More engaging loading text
        loadingSpinner.style.display = 'block'; // Show loading spinner
        resultSection.classList.remove('show'); // Hide results with transition

        const formData = new FormData(shortenForm);
        const longUrl = formData.get('long_url');
        const alias = formData.get('alias');
        const copyToClipboard = formData.get('copy_to_clipboard');
        const generateQr = formData.get('generate_qr');

        // Clear previous results and messages
        shortLinkOutput.textContent = '';
        qrCodeImage.style.display = 'none';
        qrCodeImage.src = '';
        messageDiv.style.opacity = '0'; // Start hidden for transition
        messageDiv.style.display = 'none';
        messageDiv.classList.remove('error-message');

        try {
            const response = await fetch('/shorten', {
                method: 'POST',
                body: new URLSearchParams({
                    long_url: longUrl,
                    alias: alias,
                    copy_to_clipboard: copyToClipboard,
                    generate_qr: generateQr
                }),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });

            const data = await response.json();

            if (data.error) {
                showMessage(data.error, 'error');
            } else {
                shortLinkOutput.textContent = data.short_link;
                
                if (data.qr_code_base64) {
                    qrCodeImage.src = `data:image/png;base64,${data.qr_code_base64}`;
                    qrCodeImage.style.display = 'block';
                }
                
                if (data.copied_message && copyToClipboard) { // Only show message if copied via checkbox
                    showMessage(data.copied_message, 'success');
                }

                // Clear input fields after successful shortening
                longUrlInput.value = '';
                aliasInput.value = '';
                copyToClipboardCheckbox.checked = false;
                generateQrCheckbox.checked = false;

                // Smooth scroll to results if needed and show results with transition
                if (resultSection) {
                    setTimeout(() => {
                        resultSection.classList.add('show'); // Show results with fade-in/slide-up
                        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100); // Small delay for CSS transition to apply
                }
            }

        } catch (error) {
            console.error('Error:', error);
            showMessage('An unexpected error occurred.', 'error');
        } finally {
            shortenButton.disabled = false; // Re-enable button
            shortenButton.textContent = 'Shorten URL';
            loadingSpinner.style.display = 'none'; // Hide loading spinner
        }
    });

    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.classList.remove('error-message'); // Reset error class
        if (type === 'error') {
            messageDiv.classList.add('error-message');
        }
        messageDiv.style.display = 'block';
        setTimeout(() => {
            messageDiv.style.opacity = '1'; // Fade in
        }, 10); // Small delay to trigger transition

        // Auto-hide message after a few seconds
        setTimeout(() => {
            messageDiv.style.opacity = '0'; // Fade out
            messageDiv.addEventListener('transitionend', function handler() {
                messageDiv.style.display = 'none';
                messageDiv.removeEventListener('transitionend', handler);
            });
        }, 5000); // 5 seconds
    }
});
