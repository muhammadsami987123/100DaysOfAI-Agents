document.addEventListener('DOMContentLoaded', () => {
	const form = document.getElementById('form');
	const status = document.getElementById('status');
	const results = document.getElementById('results');
	const dlSrt = document.getElementById('dl-srt');
	const dlVtt = document.getElementById('dl-vtt');
	const dlTxt = document.getElementById('dl-txt');

	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		status.textContent = 'Processing...';
		results.classList.add('hidden');

		const data = new FormData(form);
		// normalize checkboxes
		if (!data.has('auto_sync')) data.append('auto_sync', '');
		if (!data.has('speaker_labels')) data.append('speaker_labels', '');

		try {
			const res = await fetch('/api/process', { method: 'POST', body: data });
			const json = await res.json();
			if (!json.success) {
				status.textContent = json.error || 'Failed';
				return;
			}
			dlSrt.href = json.download.srt;
			dlVtt.href = json.download.vtt;
			dlTxt.href = json.download.txt;
			results.classList.remove('hidden');
			status.textContent = 'Done';
		} catch (err) {
			console.error(err);
			status.textContent = 'Error';
		}
	});
});
