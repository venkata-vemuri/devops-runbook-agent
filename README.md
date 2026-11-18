# devops-runbook-agent

A small command-line agent that answers DevOps questions from a folder of Markdown runbooks and
cites its sources. It retrieves the most relevant sections with BM25 keyword search, then asks
Claude to answer using only those sections.

## How it works
1. `retriever.py` splits each Markdown file into chunks at every heading and indexes them with BM25.
2. `agent.py` sends the top chunks to Claude as numbered sources and asks for cited answers.
3. If nothing relevant is found, the agent says so and does not call the model.

## Run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python -m runbook_agent.cli "Why is my pod in CrashLoopBackOff?"
```

## Test it (no API key needed)
```bash
pytest
```

## Roadmap
- [x] BM25 retrieval with citations
- [ ] Tool use and an MCP server for doc search
- [ ] Evaluation questions with expected answers
- [ ] Dockerfile and GitHub Actions CI
- [ ] Deploy to AWS with Terraform
