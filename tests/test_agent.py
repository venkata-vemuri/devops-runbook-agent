from types import SimpleNamespace

from runbook_agent.agent import ask
from runbook_agent.retriever import Retriever


class FakeClient:
    """Stands in for the Claude client so tests need no API key."""

    def __init__(self):
        self.last_prompt = ""
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.last_prompt = kwargs["messages"][0]["content"]
        return SimpleNamespace(
            content=[SimpleNamespace(text="Check logs with --previous [1].")],
            usage=SimpleNamespace(input_tokens=100, output_tokens=20),
        )


def test_ask_sends_sources_and_returns_citations():
    client = FakeClient()
    answer = ask("why is my pod in CrashLoopBackOff", Retriever.from_dir("docs"), client=client)
    assert "kubernetes-crashloop" in client.last_prompt
    assert answer.sources and answer.input_tokens == 100


def test_ask_without_matches_does_not_call_model():
    client = FakeClient()
    answer = ask("zzzz qqqq", Retriever.from_dir("docs"), client=client)
    assert client.last_prompt == ""
    assert "could not find" in answer.text
