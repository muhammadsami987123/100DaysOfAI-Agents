// static/script.js
// Handles UI interactivity for PhotoOrganizerAgent

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            document.getElementById('loading').style.display = 'block';
        });
    }
});
