import sys
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
from app.graph import blog_graph

def main():
    topic = " ".join(sys.argv[1:]).strip() or "How retrieval-augmented generation works"
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    initial_state = {
        "topic": topic,
        "mode": "closed_book",
        "needs_research": False,
        "queries": [],
        "evidence": [],
        "plan": None,
        "as_of": date.today().isoformat(),
        "recency_days": 3650,
        "sections": [],
        "merged_md": "",
        "final": "",
    }

    result = blog_graph.invoke(initial_state)
    print("\n--- BLOG GENERATED ---\n")
    print(result["final"])
    print(f"\nSaved output in: {output_dir.resolve()}")

if __name__ == "__main__":
    main()
