import pytest
from agent import GitHubRepoAnalyzer

@pytest.mark.asyncio
async def test_analyze():
    agent = GitHubRepoAnalyzer()
    summary = await agent.analyze("https://github.com/user/repo")
    assert isinstance(summary, str)
