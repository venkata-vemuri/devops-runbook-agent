"""Ask Claude a question, giving it only the retrieved chunks as sources."""
import os
from dataclasses import dataclass

import anthropic

from .retriever import Chunk, Retriever

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

SYSTEM = (
    "You are a DevOps runbook assistant. Answer ONLY from the numbered sources provided. "
    "Cite sources inline like [1] or [2]. If the sources do not contain the answer, say "
    "'I could not find that in the docs' and do not guess. Be concise and give concrete steps."
)


@dataclass
class Answer:
    text: str
    sources: list[Chunk]
    input_tokens: int = 0
    output_tokens: int = 0


def build_context(chunks: list[Chunk]) -> str:
    parts = [f"[{i}] ({c.source} > {c.heading})\n{c.text}" for i, c in enumerate(chunks, start=1)]
    return "\n\n".join(parts)


def ask(question: str, retriever: Retriever, client=None, k: int = 4) -> Answer:
    chunks = retriever.search(question, k=k)
    if not chunks:
        return Answer("I could not find that in the docs.", [])

    client = client or anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    prompt = f"Sources:\n\n{build_context(chunks)}\n\nQuestion: {question}"
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return Answer(
        text=response.content[0].text,
        sources=chunks,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )
