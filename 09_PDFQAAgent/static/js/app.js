let currentDocId = null;
let sessionId = null;

async function createSession() {
  const res = await fetch('/api/session', { method: 'POST' });
  const data = await res.json();
  if (data.success) sessionId = data.session_id;
}

function setDocInfo(meta) {
  const el = document.getElementById('docInfo');
  el.classList.remove('hidden');
  el.innerHTML = `
    <div class="flex items-center justify-between">
      <div>
        <div class="text-sm text-slate-500">Document loaded</div>
        <div class="font-semibold">${meta.title} <span class="text-slate-400">(${meta.media_type}, pages: ${meta.num_pages})</span></div>
        <div class="text-xs text-slate-500">doc_id: <code>${meta.doc_id}</code></div>
      </div>
      <button class="btn-primary" id="resetBtn">Load another</button>
    </div>`;
  document.getElementById('resetBtn').onclick = () => {
    currentDocId = null;
    el.classList.add('hidden');
    document.getElementById('chatContainer').classList.add('hidden');
    document.getElementById('chatBox').innerHTML = '';
    switchTab('upload');
  };
}

function appendMessage(role, text, citations) {
  const box = document.getElementById('chatBox');
  const wrapper = document.createElement('div');
  wrapper.className = `msg ${role} fade-in`;
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  wrapper.appendChild(bubble);
  if (citations && citations.length) {
    const c = document.createElement('div');
    c.className = 'citations';
    c.textContent = 'Sources: ' + citations.map(ci => `p.${ci.page ?? '-'}#${ci.chunk_index}`).join(', ');
    wrapper.appendChild(c);
  }
  box.appendChild(wrapper);
  box.scrollTop = box.scrollHeight;
}

function renderHistory(history) {
  const list = document.getElementById('historyList');
  list.innerHTML = '';
  if (!history || !history.length) {
    list.innerHTML = '<p class="text-slate-500 text-sm">No messages yet</p>';
    return;
  }
  history.forEach((h, i) => {
    const item = document.createElement('div');
    item.className = 'p-3 rounded-lg bg-white/70 border mb-2 cursor-pointer hover:bg-white transition';
    const q = (h.question || '').slice(0, 120);
    const a = (h.answer || '').slice(0, 160);
    item.innerHTML = `<div class="text-sm text-slate-700">${q}</div><div class="text-xs text-slate-500 mt-1">${a}</div>`;
    item.onclick = () => {
      const box = document.getElementById('chatBox');
      box.innerHTML = '';
      history.slice(0, i + 1).forEach(turn => {
        appendMessage('user', turn.question);
        appendMessage('assistant', turn.answer, turn.citations);
      });
    };
    list.appendChild(item);
  });
}

// Tabs logic
function switchTab(tab) {
  const uploadTab = document.getElementById('tabUpload');
  const urlTab = document.getElementById('tabUrl');
  const uploadPane = document.getElementById('paneUpload');
  const urlPane = document.getElementById('paneUrl');
  if (tab === 'upload') {
    uploadTab.classList.add('bg-white');
    urlTab.classList.remove('bg-white');
    uploadPane.classList.remove('hidden');
    urlPane.classList.add('hidden');
  } else {
    urlTab.classList.add('bg-white');
    uploadTab.classList.remove('bg-white');
    urlPane.classList.remove('hidden');
    uploadPane.classList.add('hidden');
  }
}

document.getElementById('tabUpload').addEventListener('click', () => switchTab('upload'));
document.getElementById('tabUrl').addEventListener('click', () => switchTab('url'));

// Upload handling
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
if (dropZone) {
  dropZone.addEventListener('click', () => fileInput.click());
  dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('bg-slate-100'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('bg-slate-100'));
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('bg-slate-100');
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
    }
  });
}

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!sessionId) await createSession();
  const file = fileInput.files[0];
  if (!file) return alert('Choose a file');
  const form = new FormData();
  form.append('file', file);
  form.append('session_id', sessionId);
  const res = await fetch('/api/upload', { method: 'POST', body: form });
  const data = await res.json();
  if (!data.success) return alert(data.error || 'Failed to upload');
  currentDocId = data.doc_id;
  setDocInfo(data);
  document.getElementById('chatContainer').classList.remove('hidden');
  document.getElementById('historyList').innerHTML = '<p class="text-slate-500 text-sm">No messages yet</p>';
});

// URL handling

document.getElementById('urlForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!sessionId) await createSession();
  const url = document.getElementById('urlInput').value.trim();
  if (!url) return alert('Enter a URL');
  const res = await fetch('/api/fetch_url', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url, session_id: sessionId })});
  const data = await res.json();
  if (!data.success) return alert(data.error || 'Failed to fetch URL');
  currentDocId = data.doc_id;
  setDocInfo(data);
  document.getElementById('chatContainer').classList.remove('hidden');
  document.getElementById('historyList').innerHTML = '<p class="text-slate-500 text-sm">No messages yet</p>';
});

// Chat handling

document.getElementById('chatForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const q = document.getElementById('questionInput').value.trim();
  if (!q) return;
  if (!currentDocId) return alert('Load a document first');
  appendMessage('user', q);
  document.getElementById('questionInput').value = '';
  const res = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q, doc_id: currentDocId, session_id: sessionId })});
  const data = await res.json();
  if (!data.success) return appendMessage('assistant', data.error || 'Error answering');
  appendMessage('assistant', data.answer, data.citations);
  renderHistory(data.history || []);
});

// Initialize default tab and session
switchTab('upload');
createSession().catch(() => {});
