const form = document.getElementById('tts-form');
const modeRadios = form.elements['mode'];
const textInput = document.getElementById('text-input');
const fileInput = document.getElementById('file-input');
const urlInput = document.getElementById('url-input');
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const player = document.getElementById('player');
const audioEl = document.getElementById('audio');
const downloadEl = document.getElementById('download');

function updateMode() {
  const mode = [...modeRadios].find(r => r.checked).value;
  textInput.classList.toggle('hidden', mode !== 'text');
  fileInput.classList.toggle('hidden', mode !== 'file');
  urlInput.classList.toggle('hidden', mode !== 'url');
}

[...modeRadios].forEach(radio => {
  radio.addEventListener('change', updateMode);
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorEl.classList.add('hidden');
  errorEl.textContent = '';
  loadingEl.classList.remove('hidden');
  player.classList.add('hidden');
  audioEl.src = '';

  const mode = [...modeRadios].find(r => r.checked).value;
  const formData = new FormData();
  
  // Add language and gender
  formData.append('language', document.getElementById('language').value);
  formData.append('gender', document.getElementById('gender').value);
  
  // Add the appropriate input based on mode
  if (mode === 'text') {
    const text = document.getElementById('text').value.trim();
    if (!text) {
      errorEl.textContent = 'Please enter some text';
      errorEl.classList.remove('hidden');
      loadingEl.classList.add('hidden');
      return;
    }
    formData.append('text', text);
  } else if (mode === 'file') {
    const file = document.getElementById('file').files[0];
    if (!file) {
      errorEl.textContent = 'Please select a file';
      errorEl.classList.remove('hidden');
      loadingEl.classList.add('hidden');
      return;
    }
    formData.append('file', file);
  } else if (mode === 'url') {
    const url = document.getElementById('url').value.trim();
    if (!url) {
      errorEl.textContent = 'Please enter a URL';
      errorEl.classList.remove('hidden');
      loadingEl.classList.add('hidden');
      return;
    }
    formData.append('url', url);
  }

  try {
    const response = await fetch('/api/tts', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.error || `Request failed: ${response.status}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    audioEl.src = url;
    downloadEl.href = url;
    player.classList.remove('hidden');
  } catch (err) {
    errorEl.textContent = err.message || 'Something went wrong';
    errorEl.classList.remove('hidden');
  } finally {
    loadingEl.classList.add('hidden');
  }
});

updateMode();


