document.addEventListener('DOMContentLoaded', function () {
  const output = document.getElementById('output-panel');
  const copyBtn = document.getElementById('copy-btn');
  const downloadBtn = document.getElementById('download-btn');
  const clearBtn = document.getElementById('clear-btn');
  const blobs = Array.from(document.getElementsByClassName('blob'));
  const form = document.querySelector('form.form');

  // Utility to add click effect to any button
  function addClickEffect(btn, type = 'glow') {
    if (!btn) return;
    btn.classList.add('clicked');
    // Remove after animation completes
    setTimeout(() => btn.classList.remove('clicked'), type === 'glow' ? 800 : 300);
  }

  // Copy with success animation
  copyBtn?.addEventListener('click', async () => {
    if (!output?.textContent) return;
    
    try {
      await navigator.clipboard.writeText(output.textContent);
      addClickEffect(copyBtn);
      copyBtn.classList.add('success');
      setTimeout(() => copyBtn.classList.remove('success'), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  });

  // Download with animation
  downloadBtn?.addEventListener('click', () => {
    if (!output?.textContent) return;

    const blob = new Blob([output.textContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'repo-analysis.txt';
    
    addClickEffect(downloadBtn);
    downloadBtn.style.animation = 'downloadStart 0.5s ease';
    
    // Reset animation
    setTimeout(() => {
      downloadBtn.style.animation = '';
      URL.revokeObjectURL(url);
    }, 1000);

    a.click();
  });

  function renderOutputAsList() {
    if (!output) return;
    const raw = output.textContent || '';
    // If already converted, skip
    if (output.dataset.converted === '1') return;

    // sanitize markdown and HTML artifacts before splitting into lines
    const cleanedRaw = raw
      .replace(/`+/g, '')         // remove backticks
      .replace(/\*\*/g, '')     // remove bold markers **
      .replace(/___|___/g, '')
      .replace(/(^|\s)\*\s+/g, '$1') // remove leading asterisks
      .replace(/^[-•\*\d\.\)\s]+/gm, '') // remove common list bullets/numbering at start of lines
      .replace(/\*\s+/g, '')
      .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1') // convert markdown links to text
      .replace(/<[^>]+>/g, '') // strip tags if any
      .trim();

    const lines = cleanedRaw.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    if (lines.length === 0) return;

    const ul = document.createElement('ul');
    ul.className = 'todo-list';

    lines.forEach((line, idx) => {
      const li = document.createElement('li');
      li.className = 'todo-item';
      li.style.animationDelay = `${idx * 70}ms`;

      const bullet = document.createElement('div');
      bullet.className = 'bullet';
      const text = document.createElement('div');
      text.className = 'text';
      text.textContent = line;

      li.appendChild(bullet);
      li.appendChild(text);
      ul.appendChild(li);
    });

    // Clear and replace
    output.innerHTML = '';
    output.appendChild(ul);
    output.dataset.converted = '1';

    // generate next steps based on the extracted lines
    generateNextSteps(lines);

    // hide loading overlay when results are rendered
    hideLoadingOverlay();
  }

  function showLoadingOverlay() {
    const lo = document.getElementById('loading-overlay');
    if (lo) lo.classList.remove('hidden');
  }

  function hideLoadingOverlay() {
    const lo = document.getElementById('loading-overlay');
    if (lo) lo.classList.add('hidden');
  }

  function generateNextSteps(lines) {
    const ns = document.getElementById('next-steps');
    const nsList = document.getElementById('ns-list');
    if (!ns || !nsList) return;
    nsList.innerHTML = '';

    const joined = (lines || []).join(' ').toLowerCase();
    const suggestions = new Set();

    // Heuristic keyword-based suggestions
    if (/readme|read me/.test(joined)) suggestions.add('Update README with a concise tech stack, installation and usage examples.');
    if (/test|tests|pytest|unittest|coverage/.test(joined)) suggestions.add('Add automated tests and configure CI (e.g., GitHub Actions) for continuous verification.');
    if (/dockerfile|docker|compose|container/.test(joined)) suggestions.add('Provide a Dockerfile or docker-compose for reproducible environments and easy local runs.');
    if (/license/.test(joined)) suggestions.add('Include a LICENSE file to clarify project reuse and contribution rules.');
    if (/contrib|contributing/.test(joined)) suggestions.add('Add CONTRIBUTING.md and community guidelines to help external contributors.');
    if (/requirements|dependencies|pyproject|package.json/.test(joined)) suggestions.add('Document dependencies and provide a lockfile or requirements.txt for reproducible installs.');
    if (/security|secret|vulnerab/.test(joined)) suggestions.add('Add guidance on secrets, credentials, and security recommendations (do not commit API keys).');
    if (/issue|bug|todo/.test(joined)) suggestions.add('Create a prioritized issue list and label important TODOs to guide future work.');

    // If we still have few suggestions, add helpful fallbacks
    if (suggestions.size < 3) {
      suggestions.add('Summarize the repository purpose and key links at the top of the README.');
      suggestions.add('Add a short Getting Started section with minimal steps to run locally.');
      suggestions.add('Add basic test(s) or an example script showing the primary use-case.');
    }

    // render up to 6 suggestions
    Array.from(suggestions).slice(0, 6).forEach((sText, idx) => {
      const li = document.createElement('li');
      li.className = 'ns-item';

      const bullet = document.createElement('div');
      bullet.className = 'step-bullet';

      const txt = document.createElement('div');
      txt.className = 'step-text';
      txt.textContent = sText;

      const actions = document.createElement('div');
      actions.className = 'ns-actions';
      const doneBtn = document.createElement('button');
      doneBtn.className = 'btn ghost';
      doneBtn.textContent = 'Done';
      doneBtn.addEventListener('click', () => {
        txt.style.textDecoration = txt.style.textDecoration ? '' : 'line-through';
        doneBtn.textContent = doneBtn.textContent === 'Done' ? 'Undo' : 'Done';
      });
      const copyBtnLocal = document.createElement('button');
      copyBtnLocal.className = 'btn';
      copyBtnLocal.textContent = 'Copy';
      copyBtnLocal.addEventListener('click', () => {
        navigator.clipboard && navigator.clipboard.writeText(sText).catch(()=>{});
      });

      actions.appendChild(doneBtn);
      actions.appendChild(copyBtnLocal);

      li.appendChild(bullet);
      li.appendChild(txt);
      li.appendChild(actions);
      nsList.appendChild(li);
    });

    ns.classList.remove('hidden');
  }

  function addClickEffect(btn) {
    btn.classList.add('clicked');
    setTimeout(() => btn.classList.remove('clicked'), 800);
  }

  function copyOutput() {
    if (!output) return;
    // If converted, compose text from list
    let text = '';
    if (output.dataset.converted === '1') {
      const items = output.querySelectorAll('.todo-item .text');
      text = Array.from(items).map(i => i.textContent).join('\n');
    } else {
      text = output.textContent || '';
    }
    if (!navigator.clipboard) {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { 
        document.execCommand('copy');
        addClickEffect(copyBtn);
      } catch (e) { }
      ta.remove();
      return;
    }
    navigator.clipboard.writeText(text)
      .then(() => addClickEffect(copyBtn))
      .catch(() => {});
  }

  function downloadOutput() {
    if (!output) return;
    let text = output.textContent || '';
    if (output.dataset.converted === '1') {
      const items = output.querySelectorAll('.todo-item .text');
      text = Array.from(items).map(i => i.textContent).join('\n');
    }
    const blob = new Blob([text], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'repo_analysis.txt';
    document.body.appendChild(link);
    link.click();
    link.remove();
    addClickEffect(downloadBtn);
  }

  function clearFormAndOutput() {
    const repo = document.getElementById('repo_url');
    if (repo) repo.value = '';
    if (output) { output.innerHTML = ''; output.dataset.converted = '0'; }
    const ns = document.getElementById('next-steps');
    if (ns) ns.classList.add('hidden');
  }

  // Parallax blobs based on mouse movement for subtle depth
  function onPointerMove(e) {
    const x = (e.clientX / window.innerWidth) - 0.5;
    const y = (e.clientY / window.innerHeight) - 0.5;
    blobs.forEach((b, idx) => {
      const speed = (idx + 1) * 8;
      b.style.transform = `translate3d(${x * speed}px, ${y * speed}px, 0)`;
    });
  }

  // Bind
  if (copyBtn) copyBtn.addEventListener('click', copyOutput);
  if (downloadBtn) downloadBtn.addEventListener('click', downloadOutput);
  if (clearBtn) clearBtn.addEventListener('click', clearFormAndOutput);
  if (output) renderOutputAsList();
  // show loading overlay on form submit
  const formEl = document.querySelector('form.form');
  if (formEl) {
    formEl.addEventListener('submit', function (e) {
      // show loading overlay and let the form submit; overlay will be hidden when results arrive
      showLoadingOverlay();
      const submitBtn = formEl.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
    });
    // re-enable submit when cleared
    if (clearBtn) clearBtn.addEventListener('click', () => {
      const submitBtn = formEl.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = false;
    });
  }
  window.addEventListener('pointermove', onPointerMove);

  // Re-run render when new content arrives (simple polling for spice)
  let lastText = output ? output.textContent : '';
  setInterval(() => {
    if (!output) return;
    if ((output.textContent || '') !== lastText) {
      lastText = output.textContent || '';
      // small delay to wait for server-rendered content
      setTimeout(() => { renderOutputAsList(); }, 120);
    }
  }, 800);
});
