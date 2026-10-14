# Groq + LangGraph Blog Writer

A modular refactor of the supplied multi-agent blog-writer graph. Text generation uses Groq; image generation is isolated behind a Hugging Face Inference API adapter so it can be replaced without rewriting the graph.

## Features
- Router decides whether research is useful
- Optional Tavily research
- Structured blog outline
- Parallel section-writing workers with LangGraph `Send`
- Image planning and image placement
- Markdown output saved under `output/`; generated images saved under `output/images/`

## 1. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configure keys

Copy `.env.example` to `.env` and set:
- `GROQ_API_KEY` — required for text generation
- `TAVILY_API_KEY` — optional; without it the research node returns no evidence
- `HF_TOKEN` — optional; needed for Hugging Face image inference

The exact free-tier limits and model availability depend on the provider/account. This project does not promise unlimited free image generation.

## 3. Run

```powershell
python main.py
```

Edit the `topic` in `main.py` or pass one as an argument:

```powershell
python main.py "How RAG evaluation works"
```

## Model settings

Set `GROQ_MODEL` in `.env` to a model currently available to your Groq account. The default below is only a starting point; provider model catalogs and free-tier access can change.

Set `HF_IMAGE_MODEL` to a text-to-image model supported by your Hugging Face Inference Provider/account. `black-forest-labs/FLUX.1-schnell` is the default candidate, but availability/credits can vary.

## Project structure

```text
groq_langgraph_blog_writer/
├── main.py
├── requirements.txt
├── .env.example
├── app/
│   ├── config.py
│   ├── schemas.py
│   ├── state.py
│   ├── models.py
│   ├── research.py
│   ├── nodes/
│   │   ├── routing.py
│   │   ├── planning.py
│   │   ├── writing.py
│   │   └── images.py
│   └── graph.py
└── output/
```

## Notes
- Image generation failure is handled gracefully: the Markdown keeps a clear note instead of crashing the whole blog run.
- This is a starter refactor. Review generated claims and citations before publishing.
