import pytest
from url_shortener_agent import URLShortenerAgent

@pytest.fixture
def agent():
    return URLShortenerAgent()

def test_basic_shorten(agent):
    long_url = "https://www.example.com"
    result = agent.shorten_url(long_url)
    assert result['error'] is None
    assert result['short_link'] is not None
    assert "shrtco.de" in result['short_link']

def test_custom_alias(agent):
    long_url = "https://www.google.com"
    alias = "mygooglelink"
    result = agent.shorten_url(long_url, alias=alias)
    assert result['error'] is None
    assert alias in result['short_link']

def test_invalid_url(agent):
    invalid_url = "invalid-url"
    result = agent.shorten_url(invalid_url)
    assert result['error'] is not None
    assert result['short_link'] is None

def test_qr_code_generation(agent):
    short_link = "https://shrtco.de/example"
    qr_code_base64 = agent.generate_qr_code(short_link)
    assert qr_code_base64 is not None
    assert isinstance(qr_code_base64, str)
    assert len(qr_code_base64) > 0 # Should be a non-empty base64 string
