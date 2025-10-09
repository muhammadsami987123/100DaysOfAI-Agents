document.addEventListener('DOMContentLoaded', () => {
    const getRecipesButton = document.getElementById('get-recipes');
    const ingredientsInput = document.getElementById('ingredients');
    const recipeResultsDiv = document.getElementById('recipe-results');
    const vegetarianCheckbox = document.getElementById('vegetarian');
    const veganCheckbox = document.getElementById('vegan');
    const glutenFreeCheckbox = document.getElementById('gluten-free');
    const quickMealCheckbox = document.getElementById('quick-meal');
    const mealTypeSelect = document.getElementById('meal-type');
    const voiceInputButton = document.getElementById('voice-input');
    const imageUploadInput = document.getElementById('image-upload');
    const statusIndicator = document.getElementById('status-indicator');
    const downloadSection = document.getElementById('download-section');
    const downloadRecipesButton = document.getElementById('download-recipes');

    let mediaRecorder;
    let audioChunks = [];
    let currentRecipes = []; // Store fetched recipes

    function showStatus(message, type = 'info') {
        const statusText = statusIndicator.querySelector('p');
        const loader = statusIndicator.querySelector('.loader');

        if (statusText) statusText.textContent = message;
        statusIndicator.classList.remove('hidden');
        loader.classList.remove('hidden');
        
        statusIndicator.classList.remove('text-yellow-400', 'text-red-500', 'text-green-500', 'text-blue-500');
        if (type === 'info') {
            statusIndicator.classList.add('text-blue-500');
        } else if (type === 'error') {
            statusIndicator.classList.add('text-red-500');
            loader.classList.add('hidden'); // Hide loader on error
        } else if (type === 'success') {
            statusIndicator.classList.add('text-green-500');
            loader.classList.add('hidden'); // Hide loader on success
        }
    }

    function hideStatus() {
        statusIndicator.classList.add('hidden');
    }

    function downloadRecipes() {
        if (currentRecipes.length === 0) {
            alert('No recipes to download!');
            return;
        }

        const fileName = 'recipes.json';
        const dataStr = JSON.stringify(currentRecipes, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    imageUploadInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        showStatus('Analyzing image for ingredients...', 'info');
        recipeResultsDiv.innerHTML = ''; // Clear previous results
        downloadSection.classList.add('hidden'); // Hide download button

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/upload-image-for-ingredients', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.ingredients && data.ingredients.length > 0) {
                ingredientsInput.value = data.ingredients.join(', ');
                hideStatus();
                getRecipesButton.click(); // Automatically get recipes after image input
            } else {
                showStatus('Could not detect ingredients from image. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error uploading image:', error);
            showStatus('Error processing image. Please try again.', 'error');
        }
    });

    voiceInputButton.addEventListener('click', async () => {
        if (voiceInputButton.innerHTML.includes('🎤 Voice Input')) {
            // Start recording
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                audioChunks = [];

                showStatus('Processing voice input...', 'info');
                recipeResultsDiv.innerHTML = ''; // Clear previous results
                downloadSection.classList.add('hidden'); // Hide download button

                const formData = new FormData();
                formData.append('audio', audioBlob, 'audio.webm');

                try {
                    const response = await fetch('/voice-to-text', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    if (data.transcription) {
                        ingredientsInput.value = data.transcription;
                        hideStatus();
                        getRecipesButton.click(); // Automatically get recipes after voice input
                    } else {
                        showStatus('Could not transcribe audio. Please try again.', 'error');
                    }
                } catch (error) {
                    console.error('Error processing voice input:', error);
                    showStatus('Error processing voice input. Please try again.', 'error');
                }
            };

            voiceInputButton.innerHTML = '<i class="fas fa-stop-circle mr-2"></i> 🔴 Stop Recording';
            voiceInputButton.classList.remove('bg-green-600');
            voiceInputButton.classList.add('bg-red-600');
        } else {
            // Stop recording
            mediaRecorder.stop();
            voiceInputButton.innerHTML = '<i class="fas fa-microphone mr-2"></i> 🎤 Voice Input';
            voiceInputButton.classList.remove('bg-red-600');
            voiceInputButton.classList.add('bg-green-600');
        }
    });

    getRecipesButton.addEventListener('click', async () => {
        const ingredients = ingredientsInput.value;
        const filters = {
            vegetarian: vegetarianCheckbox.checked,
            vegan: veganCheckbox.checked,
            gluten_free: glutenFreeCheckbox.checked,
            quick_meal: quickMealCheckbox.checked,
            meal_type: mealTypeSelect.value
        };

        if (!ingredients) {
            showStatus('Please enter some ingredients!', 'error');
            return;
        }

        showStatus('Loading recipes...', 'info');
        recipeResultsDiv.innerHTML = ''; // Clear previous results
        downloadSection.classList.add('hidden'); // Hide download button

        try {
            const response = await fetch('/recipes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ingredients: ingredients, filters: filters })
            });
            const recipes = await response.json();

            if (recipes.length === 0) {
                showStatus('No recipes found with your ingredients.', 'info');
                currentRecipes = [];
                return;
            }

            currentRecipes = recipes; // Store fetched recipes
            recipeResultsDiv.innerHTML = '';
            recipes.forEach((recipe, index) => {
                const recipeCard = `
                    <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-200 h-full flex flex-col justify-between">
                        <div>
                            <h2 class="text-2xl font-bold mb-3 text-blue-600">${recipe.title}</h2>
                            <p class="text-gray-700 mb-4">${recipe.description}</p>
                            ${recipe.calories ? `<p class="text-gray-600 text-sm mb-1"><i class="fas fa-fire-alt mr-2"></i><strong>Calories:</strong> ${recipe.calories}</p>` : ''}
                            ${recipe.prep_time ? `<p class="text-gray-600 text-sm mb-4"><i class="fas fa-clock mr-2"></i><strong>Preparation Time:</strong> ${recipe.prep_time} minutes</p>` : ''}
                            
                            <h3 class="text-lg font-semibold mt-4 mb-2 text-gray-800"><i class="fas fa-utensils mr-2"></i>Ingredients:</h3>
                            <ul class="list-disc list-inside space-y-1 text-gray-700">
                                ${recipe.ingredients.map(ing => `<li>${ing.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</li>`).join('')}
                            </ul>
                        </div>
                        
                        <div class="mt-6">
                            <h3 class="text-lg font-semibold mb-2 text-gray-800"><i class="fas fa-list-ol mr-2"></i>Instructions:</h3>
                            <ol class="list-decimal list-inside space-y-2 text-gray-700">
                                ${recipe.instructions.map(step => `<li>${step}</li>`).join('')}
                            </ol>
                        </div>
                    </div>
                `;
                recipeResultsDiv.innerHTML += recipeCard;
            });
            downloadSection.classList.remove('hidden'); // Show download button
            hideStatus();

        } catch (error) {
            console.error('Error fetching recipes:', error);
            showStatus('Error fetching recipes. Please try again.', 'error');
            downloadSection.classList.add('hidden'); // Hide download button on error
        }
    });

    downloadRecipesButton.addEventListener('click', downloadRecipes);
});
