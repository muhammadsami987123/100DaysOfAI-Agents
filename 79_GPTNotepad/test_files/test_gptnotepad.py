import pytest
from fastapi.testclient import TestClient
from main import app
import io

def get_client():
    return TestClient(app)

def test_manual_note():
    client = get_client()
    resp = client.post('/summarize', data={'note': 'This is a test meeting note. Action item: Schedule the next sprint by Friday.'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'summary' in data and isinstance(data['summary'], list) and data['summary']
    assert 'notes' in data and 'meeting' in data['notes'].lower()

def test_txt_file():
    client = get_client()
    file_content = b'Invoice total: $350. Please follow up with client.'
    resp = client.post('/summarize', files={'file': ('test.txt', io.BytesIO(file_content), 'text/plain')})
    assert resp.status_code == 200
    data = resp.json()
    assert 'summary' in data and data['summary']
    assert 'client' in data['notes'].lower()

def test_pdf_file():
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    # Create a fake in-memory PDF
    import tempfile
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    can = canvas.Canvas(temp.name, pagesize=letter)
    can.drawString(100,750,"Quarterly review: Revenue up 25%.")
    can.save()
    temp.seek(0)
    client = get_client()
    with open(temp.name,'rb') as f:
        pdf_bytes = f.read()
    resp = client.post('/summarize', files={'file': ('test.pdf', io.BytesIO(pdf_bytes), 'application/pdf')})
    temp.close()
    assert resp.status_code == 200
    data = resp.json()
    assert 'summary' in data and data['summary']
    assert 'quarterly' in data['notes'].lower() or 'review' in data['notes'].lower()

def test_url(monkeypatch):
    client = get_client()
    # Monkeypatch requests.get to avoid external HTTP
    class DummyResp:
        content = b'<html><body><main><h1>About Us</h1><p>Our mission is automation excellence.</p></main></body></html>'
    monkeypatch.setattr('requests.get', lambda *a,**k: DummyResp())
    resp = client.post('/summarize', data={'url':'https://example.com'})
    data = resp.json()
    assert resp.status_code == 200
    assert 'automation' in data['notes'].lower() or data['notes']
    assert isinstance(data['summary'], list) and data['summary']

def test_handles_empty():
    client = get_client()
    resp = client.post('/summarize', data={'note': ''})
    assert resp.status_code == 400 or 'Failed' in resp.text
    resp2 = client.post('/summarize', data={})
    assert resp2.status_code == 400
