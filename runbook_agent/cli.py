"""Command-line entry point: python -m runbook_agent.cli "your question" """
import argparse

from .agent import ask
from .retriever import Retriever


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the runbook agent a question.")
    parser.add_argument("question", nargs="+", help="your question")
    parser.add_argument("--docs", default="docs", help="folder of Markdown docs (default: docs)")
    parser.add_argument("-k", type=int, default=4, help="number of chunks to retrieve")
    args = parser.parse_args()

    retriever = Retriever.from_dir(args.docs)
    answer = ask(" ".join(args.question), retriever, k=args.k)

    print(answer.text)
    if answer.sources:
        print("\nSources:")
        for i, c in enumerate(answer.sources, start=1):
            print(f"  [{i}] {c.source} > {c.heading}")
        print(f"\n[tokens: in={answer.input_tokens}, out={answer.output_tokens}]")


if __name__ == "__main__":
    main()
