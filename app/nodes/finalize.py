import re
from pathlib import Path
from ..config import OUTPUT_DIR
from ..state import State


def safe_slug(title: str) -> str:
    value = re.sub(r"[^a-z0-9 _-]+", "", title.strip().lower())
    value = re.sub(r"\s+", "_", value).strip("_")
    return value or "blog"


def finalize_blog(state: State) -> dict:
    """Merge the written sections and save the final Markdown blog."""
    plan = state.get("plan")
    if plan is None:
        raise ValueError("Finalization called without a blog plan.")

    sections = [
        markdown
        for _, markdown in sorted(state.get("sections", []), key=lambda item: item[0])
    ]
    final_markdown = f"# {plan.blog_title}\n\n" + "\n\n".join(sections).strip() + "\n"

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{safe_slug(plan.blog_title)}.md"
    target.write_text(final_markdown, encoding="utf-8")

    return {"merged_md": final_markdown, "final": final_markdown}
