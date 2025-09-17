document.addEventListener('DOMContentLoaded', () => {
    const analyzeButton = document.getElementById('analyzeButton');
    const inputText = document.getElementById('inputText');
    const resultContainer = document.getElementById('resultContainer');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const summaryDiv = document.getElementById('summary');
    const toneDiv = document.getElementById('tone');
    const sentimentDiv = document.getElementById('sentiment');
    const statusIndicator = document.getElementById('statusIndicator');
    const themeToggle = document.getElementById('themeToggle');
    const lightIcon = document.getElementById('lightIcon');
    const darkIcon = document.getElementById('darkIcon');

    // Dark mode toggle functionality
    const enableDarkMode = () => {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        lightIcon.classList.add('hidden');
        darkIcon.classList.remove('hidden');
    };

    const disableDarkMode = () => {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
    };

    // Check for saved theme preference
    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }

    themeToggle.addEventListener('click', () => {
        if (document.documentElement.classList.contains('dark')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    });

    // Initial state setup
    const setInitialState = () => {
        inputText.value = '';
        inputText.disabled = false;
        analyzeButton.disabled = false;
        loadingIndicator.classList.add('hidden');
        resultContainer.classList.add('hidden');
        resultContainer.classList.remove('error');
        summaryDiv.textContent = '';
        toneDiv.textContent = '';
        sentimentDiv.textContent = '';
        statusIndicator.textContent = 'Ready to analyze';
        statusIndicator.classList.remove('text-red-500', 'text-green-500', 'text-blue-500', 'dark:text-red-400', 'dark:text-blue-400'); // Clear any previous status colors
        statusIndicator.classList.add('text-gray-700', 'dark:text-gray-300');
    };

    setInitialState(); // Call on page load

    analyzeButton.addEventListener('click', async () => {
        const text = inputText.value;
        if (!text.trim()) {
            resultContainer.classList.remove('hidden');
            resultContainer.classList.add('error');
            resultContainer.innerHTML = '<h2>Error:</h2><p>Please enter some text to analyze.</p>';
            statusIndicator.textContent = 'Input required';
            statusIndicator.classList.remove('text-gray-700', 'dark:text-gray-300', 'text-blue-500', 'dark:text-blue-400');
            statusIndicator.classList.add('text-red-500', 'dark:text-red-400');
            return;
        }

        // Update status indicator
        statusIndicator.textContent = 'Analyzing...';
        statusIndicator.classList.remove('text-gray-700', 'dark:text-gray-300', 'text-red-500', 'dark:text-red-400');
        statusIndicator.classList.add('text-blue-500', 'dark:text-blue-400');

        // Disable input and button during analysis
        inputText.disabled = true;
        analyzeButton.disabled = true;

        resultContainer.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
        resultContainer.classList.remove('error');
        summaryDiv.textContent = '';
        toneDiv.textContent = '';
        sentimentDiv.textContent = '';

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });
            console.log('Fetch response:', response);

            const data = await response.json();
            console.log('Parsed data:', data);

            if (response.ok) {
                const resultText = data.result;
                console.log('Result text from backend:', resultText);

                const summaryMatch = resultText.match(/Summary: ([^\r\n]+)/);
                const toneMatch = resultText.match(/Tone: ([^\r\n]+)/);
                const sentimentMatch = resultText.match(/Sentiment: ([^\r\n]+)/);

                console.log('Summary match:', summaryMatch);
                console.log('Tone match:', toneMatch);
                console.log('Sentiment match:', sentimentMatch);

                summaryDiv.textContent = `Summary: ${summaryMatch ? summaryMatch[1] : 'N/A'}`;
                toneDiv.textContent = `Tone: ${toneMatch ? toneMatch[1] : 'N/A'}`;
                sentimentDiv.textContent = `Sentiment: ${sentimentMatch ? sentimentMatch[1] : 'N/A'}`;

                resultContainer.classList.remove('hidden');
            } else {
                resultContainer.classList.remove('hidden');
                resultContainer.classList.add('error');
                resultContainer.innerHTML = `<h2>Error:</h2><p>${data.error || 'An unknown error occurred.'}</p>`;
                statusIndicator.textContent = 'Analysis failed';
                statusIndicator.classList.remove('text-blue-500', 'dark:text-blue-400');
                statusIndicator.classList.add('text-red-500', 'dark:text-red-400');
            }
        } catch (error) {
            console.error('Error during analysis:', error);
            resultContainer.classList.remove('hidden');
            resultContainer.classList.add('error');
            resultContainer.innerHTML = '<h2>Error:</h2><p>Failed to connect to the server. Please try again later.</p>';
            statusIndicator.textContent = 'Connection error';
            statusIndicator.classList.remove('text-blue-500', 'dark:text-blue-400');
            statusIndicator.classList.add('text-red-500', 'dark:text-red-400');
        } finally {
            loadingIndicator.classList.add('hidden');
            // Re-enable input and button after analysis
            inputText.disabled = false;
            analyzeButton.disabled = false;
            // Set back to ready if not an error state
            if (!resultContainer.classList.contains('error')) {
                statusIndicator.textContent = 'Ready to analyze';
                statusIndicator.classList.remove('text-blue-500', 'dark:text-blue-400', 'text-red-500', 'dark:text-red-400');
                statusIndicator.classList.add('text-gray-700', 'dark:text-gray-300');
            }
        }
    });
});
