// JavaScript for frontend interactivity will go here

document.addEventListener('DOMContentLoaded', () => {
    const generateForm = document.getElementById('generate-form');
    const flashcardsOutput = document.getElementById('flashcards-output');
    const downloadMarkdownBtn = document.getElementById('download-markdown');
    const downloadJsonBtn = document.getElementById('download-json');
    const downloadCsvBtn = document.getElementById('download-csv');

    let generatedFlashcards = []; // To store flashcards for download

    if (generateForm) {
        generateForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(generateForm);
            flashcardsOutput.innerHTML = '<p>Generating flashcards...</p>';
            generatedFlashcards = []; // Clear previous flashcards

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData,
                });

                console.log('Response status:', response.status);
                console.log('Response OK:', response.ok);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Received data:', data);
                generatedFlashcards = data.flashcards; // Store for download
                displayFlashcards(generatedFlashcards);
            } catch (error) {
                console.error('Error:', error);
                flashcardsOutput.innerHTML = `<p class="text-red-500">Error generating flashcards: ${error.message}</p>`;
            }
        });
    }

    function displayFlashcards(flashcards) {
        console.log('Displaying flashcards:', flashcards);
        if (!flashcards || flashcards.length === 0) {
            flashcardsOutput.innerHTML = '<p>No flashcards generated.</p>';
            return;
        }

        flashcardsOutput.innerHTML = '';
        flashcards.forEach((card, index) => {
            let cardHtml = '';
            if (card.type === 'qa') {
                cardHtml = `
                    <div class="flashcard-item bg-white p-4 rounded shadow-md mb-4">
                        <div class="flashcard-question font-semibold cursor-pointer" data-card-id="${index}">
                            Q: ${card.question}
                        </div>
                        <div class="flashcard-answer mt-2 hidden" id="answer-${index}">
                            A: ${card.answer}
                        </div>
                    </div>
                `;
            } else if (card.type === 'fill_in_the_blanks') {
                cardHtml = `
                    <div class="flashcard-item bg-white p-4 rounded shadow-md mb-4">
                        <div class="flashcard-question font-semibold cursor-pointer" data-card-id="${index}">
                            Fill in the blank: ${card.sentence.replace(card.blank_word, '_________')}
                        </div>
                        <div class="flashcard-answer mt-2 hidden" id="answer-${index}">
                            Answer: ${card.blank_word}
                        </div>
                    </div>
                `;
            } else if (card.type === 'true_false') {
                cardHtml = `
                    <div class="flashcard-item bg-white p-4 rounded shadow-md mb-4">
                        <div class="flashcard-question font-semibold cursor-pointer" data-card-id="${index}">
                            True or False: ${card.statement}
                        </div>
                        <div class="flashcard-answer mt-2 hidden" id="answer-${index}">
                            Answer: ${card.is_true ? 'True' : 'False'}
                        </div>
                    </div>
                `;
            }
            flashcardsOutput.innerHTML += cardHtml;
        });

        document.querySelectorAll('.flashcard-question').forEach(question => {
            question.addEventListener('click', (event) => {
                const cardId = event.target.dataset.cardId;
                const answer = document.getElementById(`answer-${cardId}`);
                if (answer) {
                    answer.classList.toggle('hidden');
                }
            });
        });
    }

    // Download functions
    function downloadFile(filename, content, type) {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    downloadMarkdownBtn.addEventListener('click', () => {
        console.log('Download Markdown clicked. Flashcards:', generatedFlashcards);
        let mdContent = generatedFlashcards.map(card => {
            if (card.type === 'qa') {
                return `### Q: ${card.question}\n**A:** ${card.answer}\n`;
            } else if (card.type === 'fill_in_the_blanks') {
                return `### Fill in the blank: ${card.sentence.replace(card.blank_word, '_________')}\n**Answer:** ${card.blank_word}\n`;
            } else if (card.type === 'true_false') {
                return `### True or False: ${card.statement}\n**Answer:** ${card.is_true ? 'True' : 'False'}\n`;
            }
            return '';
        }).join('\n---\n\n');
        downloadFile('flashcards.md', mdContent, 'text/markdown');
    });

    downloadJsonBtn.addEventListener('click', () => {
        console.log('Download JSON clicked. Flashcards:', generatedFlashcards);
        downloadFile('flashcards.json', JSON.stringify(generatedFlashcards, null, 2), 'application/json');
    });

    downloadCsvBtn.addEventListener('click', () => {
        console.log('Download CSV clicked. Flashcards:', generatedFlashcards);
        if (generatedFlashcards.length === 0) return;

        let csvContent = "Type,Question/Statement,Answer/Blank Word,Is True\n";
        generatedFlashcards.forEach(card => {
            let question = '';
            let answer = '';
            let isTrue = '';

            if (card.type === 'qa') {
                question = `"${card.question.replace(/"/g, '""')}"`;
                answer = `"${card.answer.replace(/"/g, '""')}"`;
            } else if (card.type === 'fill_in_the_blanks') {
                question = `"${card.sentence.replace(/"/g, '""')}"`;
                answer = `"${card.blank_word.replace(/"/g, '""')}"`;
            } else if (card.type === 'true_false') {
                question = `"${card.statement.replace(/"/g, '""')}"`;
                isTrue = card.is_true ? 'True' : 'False';
            }
            csvContent += `${card.type},${question},${answer},${isTrue}\n`;
        });
        downloadFile('flashcards.csv', csvContent, 'text/csv');
    });
});
