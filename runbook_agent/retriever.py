"""Load Markdown docs, split them into chunks by heading, and search with BM25."""
import re
from dataclasses import dataclass
from pathlib import Path

from rank_bm25 import BM25Okapi

TOKEN_RE = re.compile(r"[a-z0-9_]+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass
class Chunk:
    source: str   # file path, shown as the citation
    heading: str  # nearest heading above the text
    text: str
    title: str = ""  # the file's top "# Title", so every chunk knows what it is about


STOPWORDS = {"a", "an", "and", "the", "is", "are", "my", "in", "on", "of", "to", "why", "how", "do", "i", "it", "for", "what"}


def tokenize(text: str) -> list[str]:
    """Lowercase words, minus filler words like 'why' and 'is' that match everything."""
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


def split_markdown(source: str, content: str) -> list[Chunk]:
    """Split one Markdown file into chunks, starting a new chunk at every heading."""
    chunks: list[Chunk] = []
    heading = "(top)"
    title = ""
    lines: list[str] = []

    def flush() -> None:
        body = "\n".join(lines).strip()
        if body:
            chunks.append(Chunk(source=source, heading=heading, text=body, title=title))

    for line in content.splitlines():
        match = HEADING_RE.match(line)
        if match:
            flush()
            heading = match.group(2).strip()
            if len(match.group(1)) == 1 and not title:
                title = heading
            lines = []
        else:
            lines.append(line)
    flush()
    return chunks


def load_chunks(docs_dir: str | Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(Path(docs_dir).rglob("*.md")):
        content = path.read_text(encoding="utf-8", errors="ignore")
        chunks.extend(split_markdown(str(path), content))
    return chunks


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        # Include the file title and heading in the searchable text so they help ranking.
        self._index = BM25Okapi([tokenize(f"{c.title} {c.heading} {c.text}") for c in chunks]) if chunks else None

    @classmethod
    def from_dir(cls, docs_dir: str | Path) -> "Retriever":
        return cls(load_chunks(docs_dir))

    def search(self, query: str, k: int = 4) -> list[Chunk]:
        if not self._index:
            return []
        scores = self._index.get_scores(tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self.chunks[i] for i in ranked[:k] if scores[i] > 0]
