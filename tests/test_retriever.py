from runbook_agent.retriever import Retriever, split_markdown


def test_split_markdown_by_heading():
    chunks = split_markdown("a.md", "# Title\nintro\n\n## Fix\nrestart it\n")
    assert [c.heading for c in chunks] == ["Title", "Fix"]
    assert chunks[1].text == "restart it"


def test_search_finds_relevant_doc():
    r = Retriever.from_dir("docs")
    top = r.search("pod keeps restarting OOMKilled exit code 137", k=1)[0]
    assert "kubernetes-crashloop" in top.source


def test_search_state_lock():
    r = Retriever.from_dir("docs")
    top = r.search("Error acquiring the state lock", k=1)[0]
    assert "terraform-state-lock" in top.source


def test_search_unrelated_returns_nothing():
    r = Retriever.from_dir("docs")
    assert r.search("zzzz qqqq", k=3) == []
