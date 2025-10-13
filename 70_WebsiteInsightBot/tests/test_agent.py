import pytest
import os
import agent

# --- Patch Gemini call to not hit API during tests ---
def fake_llm(context, long_form):
    if 'français' in context:
        return (
            'Website Summary:\nCeci est un résumé.\nTop Keywords:\nclé, test\nSentiment:\nNeutral — factual.'
        )
    if long_form:
        return 'Website Summary:\nA long summary.\nTop Keywords:\none, two, three\nSentiment:\nPositive — optimistic.'
    return 'Website Summary:\nShort summary.\nTop Keywords:\none, two\nSentiment:\nNeutral — objective.'


def setup_module(module):
    agent.call_gemini_llm = fake_llm

def test_reachable_url(monkeypatch):
    monkeypatch.setattr(agent, 'fetch_visible_text', lambda url: 'A reachable site with text to summarize.')
    result = agent.website_insight_bot('http://site.com')
    assert result['summary'] == 'Short summary.'
    assert 'one' in result['keywords']

def test_unreachable_url():
    result = agent.website_insight_bot('http://doesnotexist.abc')
    assert 'unreachable' in result['error'].lower()

def test_empty_content(monkeypatch):
    monkeypatch.setattr(agent, 'fetch_visible_text', lambda url: '__EMPTY__')
    result = agent.website_insight_bot('http://site.com')
    assert 'No valuable' in result['error']

def test_non_english(monkeypatch):
    monkeypatch.setattr(agent, 'fetch_visible_text', lambda url: 'Ceci est du texte en français')
    result = agent.website_insight_bot('http://site.com')
    assert 'Ceci est un résumé.' in result['summary']

def test_long_form(monkeypatch):
    monkeypatch.setattr(agent, 'fetch_visible_text', lambda url: 'Some big content')
    result = agent.website_insight_bot('http://site.com', long_form=True)
    assert result['summary'] == 'A long summary.'
    assert 'optimistic' in result['sentiment']
