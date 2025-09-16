(() => {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('imageFile');
  const fileName = document.getElementById('fileName');
  const previewList = document.getElementById('previewList');

  const language = document.getElementById('language');
  const style = document.getElementById('style');
  const length = document.getElementById('length');
  const hashtags = document.getElementById('hashtags');
  const tone = document.getElementById('tone');
  const variations = document.getElementById('variations');
  const generateBtn = document.getElementById('generate');
  const genSpinner = document.getElementById('genSpinner');
  const status = document.getElementById('status');
  const resultsWrap = document.getElementById('resultsWrap');
  const saveAllTxt = document.getElementById('saveAllTxt');
  const saveAllJson = document.getElementById('saveAllJson');
  const saveAllMd = document.getElementById('saveAllMd');
  const toastHost = document.getElementById('toastHost');
  const filters = {
    All: document.getElementById('filterAll'),
    instagram: document.getElementById('filterInstagram'),
    linkedin: document.getElementById('filterLinkedin'),
    facebook: document.getElementById('filterFacebook'),
    twitter: document.getElementById('filterTwitter'),
    whatsapp: document.getElementById('filterWhatsapp'),
    tiktok: document.getElementById('filterTiktok'),
  };

  let lastResults = [];
  let activePlatform = 'All';

  function setStatus(text){ status.textContent = text; }
  function clearPreviews(){ previewList.innerHTML = ''; }
  function addPreview(file, dataUrl, index) {
    console.log("addPreview called with:", file.name, index); // Log 1
    const wrap = document.createElement('div');
    wrap.className = 'rounded-xl overflow-hidden bg-black/20 relative group';
    wrap.dataset.index = index;
    const img = document.createElement('img');
    img.src = dataUrl; img.alt = file.name; img.className = 'w-full h-40 object-cover';
    const overlay = document.createElement('div');
    overlay.className = 'absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity';
    const removeBtn = document.createElement('button');
    removeBtn.className = 'bg-red-500 text-white p-2 rounded-full text-xs';
    removeBtn.textContent = 'Remove';
    removeBtn.onclick = () => {
      filesToUpload.splice(index, 1);
      renderPreviews();
    };
    overlay.appendChild(removeBtn);
    wrap.appendChild(img);
    wrap.appendChild(overlay);
    previewList.appendChild(wrap);
  }
  let filesToUpload = [];

  function renderPreviews() {
    console.log("renderPreviews called. filesToUpload:", filesToUpload.length); // Log 1
    clearPreviews();
    if (filesToUpload.length === 0) {
      fileName.textContent = 'No files selected';
      console.log("renderPreviews: No files to render. Aborting."); // Log 2
      return;
    }
    fileName.textContent = `${filesToUpload.length} file(s) selected`;
    console.log("renderPreviews: Rendering previews for", filesToUpload.length, "files."); // Log 3
    for (let i = 0; i < filesToUpload.length; i++) {
      const file = filesToUpload[i];
      const reader = new FileReader();
      reader.onload = (e) => { addPreview(file, e.target.result, i); };
      reader.readAsDataURL(file);
    }
  }

  function renderResults(results){
    resultsWrap.innerHTML = '';
    resultsWrap.classList.remove('hidden');
    const groupedResults = results.reduce((acc, item) => {
      if (!acc[item.title]) {
        acc[item.title] = {
          filename: item.title,
          platforms: {},
        };
      }
      if (!acc[item.title].platforms[item.platform]) {
        acc[item.title].platforms[item.platform] = [];
      }
      acc[item.title].platforms[item.platform].push(item);
      return acc;
    }, {});

    Object.values(groupedResults).forEach(item => {
      const card = document.createElement('div');
      card.className = 'md-box rounded-xl p-4';
      const title = document.createElement('div');
      title.className = 'text-sm text-slate-300 mb-2';
      title.textContent = item.filename;
      card.appendChild(title);

      const grid = document.createElement('div');
      grid.className = 'grid grid-cols-1 md:grid-cols-2 gap-3';

      const platforms = ['instagram','linkedin','facebook','twitter','whatsapp','tiktok'];
      platforms.forEach(p => {
        if(activePlatform !== 'All' && activePlatform !== p) return;
        const platformCaptions = item.platforms[p] || [];
        if(platformCaptions.length === 0) return; // Don't render empty platform blocks

        const block = document.createElement('div');
        block.className = 'rounded-lg bg-white/5 border border-white/10 p-3';
        const h = document.createElement('div');
        h.className = 'text-xs uppercase tracking-wide text-slate-400 mb-2'; h.textContent = p;
        block.appendChild(h);
        const list = document.createElement('div'); list.className = 'space-y-2';

        platformCaptions.forEach(captionData => {
          const row = document.createElement('div');
          row.className = 'rounded bg-white/4 border border-white/10 p-2 text-sm text-slate-100';
          const txt = document.createElement('div');
          txt.textContent = captionData.caption;
          const hashtags = document.createElement('div');
          hashtags.className = 'text-xs text-slate-400 mt-1';
          hashtags.textContent = (captionData.hashtags || []).join(' ');

          const actions = document.createElement('div');
          actions.className = 'mt-1 text-right';
          const copyBtn = document.createElement('button');
          copyBtn.className = 'px-2 py-1 bg-white/10 rounded text-xs';
          copyBtn.textContent = 'Copy';
          copyBtn.onclick = async () => { try { await navigator.clipboard.writeText(captionData.caption + ' ' + (captionData.hashtags || []).join(' ')); copyBtn.textContent='Copied'; setTimeout(()=>copyBtn.textContent='Copy', 1000); } catch {} };
          actions.appendChild(copyBtn);

          row.appendChild(txt);
          if (captionData.hashtags && captionData.hashtags.length > 0) {
            row.appendChild(hashtags);
          }
          row.appendChild(actions);
          list.appendChild(row);
        });

        block.appendChild(list);
        grid.appendChild(block);
      });

      card.appendChild(grid);
      resultsWrap.appendChild(card);
    });
  }

  // Drag & drop handlers
  ['dragenter','dragover'].forEach(ev => {
    dropzone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); dropzone.classList.add('dragover'); });
  });
  ;['dragleave','drop'].forEach(ev => {
    dropzone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); dropzone.classList.remove('dragover'); });
  });
  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('drop', e => { const files = Array.from(e.dataTransfer.files || []); if(files.length) handleFiles(files); });
  fileInput.addEventListener('change', e => { const files = Array.from(e.target.files || []); if(files.length) handleFiles(files); });

  async function handleFiles(newFiles) {
    console.log("handleFiles called with:", newFiles); // Log 1
    const validFiles = Array.from(newFiles).filter(f => f.type.startsWith('image/')).slice(0, 10);
    if (!validFiles.length) {
      showToast('Please choose image files (JPG, PNG, WEBP).', 'error');
      console.log("handleFiles: No valid files. Aborting."); // Log 2
      return;
    }
    filesToUpload = validFiles;
    console.log("handleFiles: filesToUpload updated:", filesToUpload); // Log 3
    renderPreviews();
    setStatus('Images selected');
    fileInput.value = ''; // Reset file input to allow re-uploading same files
    console.log("handleFiles: fileInput value reset."); // Log 4
  }

  // Update variations count display
  variations.addEventListener('input', () => {
    document.getElementById('variationsCount').textContent = variations.value;
  });

  document.getElementById('clearAllBtn').addEventListener('click', () => {
    filesToUpload = [];
    renderPreviews();
    setStatus('Idle');
    resultsWrap.classList.add('hidden');
  });

  async function generateCaption(){
    if(filesToUpload.length === 0){ showToast('Please select images first.', 'error'); return; }
    setStatus('Generating captions...');
    generateBtn.disabled = true;
    genSpinner.classList.remove('hidden');
    resultsWrap.classList.add('hidden');
    resultsWrap.innerHTML='';
    lastResults = []; // This will now hold the flattened array of caption objects
    showToast('Generating captions...', 'info');
    try{
      const form = new FormData();
      filesToUpload.forEach(f => form.append('images', f));
      form.append('language', language.value);
      form.append('tone', tone.value);
      form.append('variations', variations.value);
      form.append('temperature', '0.95');
      const resp = await fetch('/api/captions/batch', { method: 'POST', body: form });
      const data = await resp.json();
      if(!resp.ok){ throw new Error(data.error || 'Failed to generate captions.'); }
      lastResults = data || []; // The API now returns the flattened list directly
      renderResults(lastResults);
      setStatus('Ready');
      showToast('Captions generated successfully!', 'success');
    }catch(err){
      setStatus('Error'); showToast(err.message || String(err), 'error');
    }finally{
      generateBtn.disabled = false; genSpinner.classList.add('hidden');
    }
  }

  function downloadFile(name, content, type='text/plain'){
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 500);
  }

  function showToast(message, kind='info'){
    if(!toastHost) return;
    const el = document.createElement('div');
    const color = kind==='success' ? 'bg-emerald-500/90' : kind==='error' ? 'bg-rose-500/90' : 'bg-slate-700/90';
    el.className = `${color} text-white text-sm px-3 py-2 rounded-lg shadow`;
    el.textContent = message;
    toastHost.appendChild(el);
    setTimeout(()=> el.remove(), 2400);
  }

  // Actions
  generateBtn.addEventListener('click', e => { e.preventDefault(); generateCaption(); });
  Object.entries(filters).forEach(([plat, el]) => {
    if(!el) return;
    el.addEventListener('click', () => {
      activePlatform = plat;
      Object.values(filters).forEach(b => b && b.classList.remove('active'));
      el.classList.add('active');
      renderResults(lastResults);
    });
  });
  function flattenCaptions(results){
    return results.map(item => `[${item.title}] [${item.platform}] ${item.caption} ${(item.hashtags || []).join(' ')}`);
  }

  saveAllTxt.addEventListener('click', () => { if(!lastResults.length) return; const lines = flattenCaptions(lastResults).join('\n'); downloadFile('captions.txt', lines, 'text/plain'); });
  saveAllJson.addEventListener('click', () => { if(!lastResults.length) return; downloadFile('captions.json', JSON.stringify({results: lastResults}, null, 2), 'application/json'); });
  saveAllMd.addEventListener('click', () => { if(!lastResults.length) return; 
    let md = '# Generated Captions\n\n';
    const groupedByFilename = lastResults.reduce((acc, item) => {
      if (!acc[item.title]) {
        acc[item.title] = [];
      }
      acc[item.title].push(item);
      return acc;
    }, {});

    Object.entries(groupedByFilename).forEach(([filename, captions]) => {
      md += `## ${filename}\n\n`;
      const groupedByPlatform = captions.reduce((acc, item) => {
        if (!acc[item.platform]) {
          acc[item.platform] = [];
        }
        acc[item.platform].push(item);
        return acc;
      }, {});

      Object.entries(groupedByPlatform).forEach(([platform, platformCaptions]) => {
        md += `### ${platform}\n\n`;
        platformCaptions.forEach(cap => {
          md += `- ${cap.caption} ${(cap.hashtags || []).join(' ')}\n`;
        });
        md += '\n';
      });
    });
    downloadFile('captions.md', md, 'text/markdown');
  });
})();


