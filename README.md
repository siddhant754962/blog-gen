🩷 PinkPaper AI — AI-Powered Blog Writer

An AI-powered technical blog writing application built with Python, LangGraph, LangChain, Groq, Tavily, and Streamlit. It transforms a topic into a structured blog through a multi-step workflow involving intelligent routing, optional web research, planning, section-wise writing, and finalization.

🌐 Live Demo: https://blog-gen-sidd.streamlit.app/

---

✨ Features

- 🤖 AI-Powered Blog Generation — Generate structured technical blog posts from a topic.
- 🧠 LangGraph Workflow — Organize content generation into specialized nodes.
- 🔎 Research-Assisted Writing — Retrieve web search results using Tavily when research is needed.
- 🗺️ Structured Blog Planning — Create outlines with section goals, bullet points, word targets, and writing requirements.
- ✍️ Section-Wise Generation — Generate individual blog sections using dedicated worker tasks.
- 🔗 Evidence-Based Citations — Use supplied research sources to support external claims.
- 📝 Markdown Output — Generate blog content in Markdown format.
- ☁️ Cloud Deployment — Access the application through Streamlit Community Cloud.

🛠️ Tech Stack

Technology| Purpose
Python| Core programming language
LangGraph| Workflow orchestration, state management, and task routing
LangChain| LLM integration and message handling
Groq| Language model inference
Tavily Search| Web research and source retrieval
Pydantic| Structured data models and validation
Streamlit| Interactive web application
Git & GitHub| Version control and source code management

🏗️ Architecture

PinkPaper AI uses a graph-based workflow rather than relying on a single LLM request.

                 ┌──────────────┐
                 │     START    │
                 └──────┬───────┘
                        ▼
                 ┌──────────────┐
                 │    Router    │
                 └──────┬───────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌────────────┐      ┌──────────────┐
       │  Research  │      │ Orchestrator │
       └─────┬──────┘      └──────┬───────┘
             │                    │
             └─────────┬──────────┘
                       ▼
               ┌──────────────┐
               │ Orchestrator │
               │ creates plan │
               └──────┬───────┘
                      ▼
               ┌──────────────┐
               │ Worker Tasks │
               │ Section-wise │
               │   writing    │
               └──────┬───────┘
                      ▼
               ┌──────────────┐
               │   Finalize   │
               └──────┬───────┘
                      ▼
                 ┌────────────┐
                 │    END     │
                 └────────────┘

Workflow overview:

1. Router: Determines the writing mode and whether research is required.
2. Research: Retrieves search results through Tavily when selected.
3. Orchestrator: Creates a structured blog plan using the LLM.
4. Worker Tasks: Write individual sections based on their assigned goals and requirements.
5. Finalize: Combines the generated sections into the final blog.

«The router can send a request directly to the orchestrator when research is unnecessary.»

📂 Project Structure

The application uses a modular Python structure.

blog-gen/
├── app.py
├── app/
│   ├── graph.py
│   ├── state.py
│   ├── schemas.py
│   ├── models.py
│   ├── config.py
│   ├── research.py
│   └── nodes/
│       ├── routing.py
│       ├── planning.py
│       ├── writing.py
│       └── finalize.py
├── requirements.txt
├── .env.example
└── README.md

Note: This is the expected structure based on the project files discussed. Adjust it to match your actual repository.

⚙️ Getting Started

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd blog-gen

Replace "YOUR_GITHUB_REPOSITORY_URL" with your repository's actual URL.

2. Create a virtual environment

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a ".env" file in the project root:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_supported_groq_model_id
TAVILY_API_KEY=your_tavily_api_key

Obtain credentials from:

- Groq: https://console.groq.com/keys
- Tavily: https://app.tavily.com/

Use a model ID currently supported by your Groq account. The application may work differently depending on model availability and rate limits.

Security: Never commit your ".env" file or expose API keys in your repository.

5. Run the application

streamlit run app.py

Open the local URL displayed in your terminal.

🧠 Core Concepts Demonstrated

LangGraph State Management

Shared state carries information between workflow stages, including the topic, research queries, evidence, plan, generated sections, and final output.

Conditional Routing

The router determines whether a topic should proceed through research or move directly to planning.

Fan-Out with "Send"

The planning stage creates multiple writing tasks. LangGraph's "Send" mechanism dispatches each task to a worker node.

Structured Outputs

Pydantic schemas define the expected shape of objects such as "Plan", "Task", and "EvidenceItem".

Retrieval-Assisted Content Generation

When research is selected, search results provide supporting material that workers can use when generating research-based sections.

⚠️ Limitations

- Generated content may contain inaccurate claims and should be reviewed before publication.
- Search results may be incomplete or outdated.
- LLM requests can fail because of provider rate limits, model availability, or API errors.
- Parallel section generation may increase token consumption.
- Citation presence does not automatically guarantee that a source supports the associated claim.

🚀 Future Improvements

- Add concurrency controls and more robust rate-limit handling.
- Validate citations against retrieved source material.
- Add automated tests for graph routing and section assembly.
- Improve observability with per-node logs and token usage metrics.
- Add persistent blog history and project-level storage.
- Support more model providers.
- Improve content quality evaluation and automated fact-checking.

🎯 What I Learned

Building PinkPaper AI helped me explore:

- Designing multi-step LLM applications with LangGraph.
- Managing state across graph nodes.
- Structuring LLM outputs with Pydantic.
- Integrating external web search into AI workflows.
- Building section-based content-generation pipelines.
- Deploying and troubleshooting an AI application in the cloud.
- Handling API failures and token rate limits.

🌐 Live Application

Try PinkPaper AI: https://blog-gen-sidd.streamlit.app/

👨‍💻 Author

Siddhant Kumar Patel

B.Tech Computer Science / Information Technology | Aspiring AI Engineer

- "GitHub" (https://github.com/siddhant754962)
- "LinkedIn" (https://www.linkedin.com/in/siddhnat-kumar-patel-699b8a251)
- "Portfolio" (https://staticfile-59ccf.wasmer.app/)

---

⭐ If you find this project interesting, consider giving the repository a star!

Built to explore practical applications of LLMs, agentic workflows, and AI-assisted content generation.
