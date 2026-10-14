import os
import re
import time
from datetime import date
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from app.graph import blog_graph

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Page setup ----------
st.set_page_config(
    page_title="PINK//PAPER — AI Blog Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Premium pink / black UI ----------
st.markdown(
    r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --pink:#ff2e93; --hot:#ff4db8; --violet:#a855f7; --bg:#07060a; --panel:#100d14; --line:#29202f; --muted:#a69aaa; }
    html, body, [class*="css"] { font-family:'Manrope',sans-serif; }
    .stApp { background:
      radial-gradient(ellipse at 70% 0%, rgba(255,46,147,.13), transparent 34%),
      radial-gradient(ellipse at 0% 55%, rgba(168,85,247,.08), transparent 28%), #07060a; color:#f8f2fa; }
    [data-testid="stHeader"] { background:rgba(7,6,10,.72); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#100b13,#09070c); border-right:1px solid #30202f; }
    [data-testid="stSidebar"] > div { padding-top:1.3rem; }
    .brand { font-size:1.05rem; font-weight:800; letter-spacing:.14em; color:#fff; }
    .brand span { color:var(--pink); }
    .eyebrow { color:#ff78bd; font:500 .72rem 'DM Mono',monospace; letter-spacing:.16em; text-transform:uppercase; }
    .hero { position:relative; overflow:hidden; padding:30px 32px; border:1px solid #392238; border-radius:24px;
      background:linear-gradient(115deg,rgba(25,12,26,.97),rgba(13,9,17,.94) 58%,rgba(45,9,34,.9));
      box-shadow:0 18px 65px rgba(0,0,0,.25), inset 0 1px rgba(255,255,255,.04); margin-bottom:22px; }
    .hero:after { content:"✦"; position:absolute; right:6%; top:-50px; font-size:190px; line-height:1; color:rgba(255,46,147,.10); transform:rotate(15deg); }
    .hero h1 { font-size:clamp(2rem,3.6vw,3.35rem); line-height:1.08; margin:.55rem 0 .65rem; letter-spacing:-.055em; font-weight:800; }
    .gradient { background:linear-gradient(90deg,#ff66b5,#ff2e93,#c084fc); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero p { color:#bcaec2; max-width:650px; font-size:1rem; margin:0; }
    .panel { background:linear-gradient(145deg,rgba(20,15,24,.97),rgba(12,10,15,.97)); border:1px solid #302432; border-radius:20px; padding:21px; box-shadow:0 14px 45px rgba(0,0,0,.18); }
    .panel-title { font-weight:750; font-size:1rem; margin-bottom:14px; display:flex; align-items:center; gap:9px; }
    .pink-dot { width:8px;height:8px;border-radius:50%;background:#ff2e93;box-shadow:0 0 14px #ff2e93;display:inline-block; }
    .small-muted { color:#a69aaa; font-size:.82rem; }
    .metric { background:#100d14; border:1px solid #302432; border-radius:15px; padding:15px 16px; min-height:91px; }
    .metric-label { color:#a69aaa; font-size:.75rem; letter-spacing:.06em; text-transform:uppercase; }
    .metric-value { color:#fff; font-size:1.5rem; font-weight:800; margin-top:4px; }
    .metric-value span { color:#ff4db8; }
    .step { display:flex; gap:12px; align-items:flex-start; padding:13px 12px; border:1px solid #2a202d; border-radius:13px; background:rgba(255,255,255,.018); margin:8px 0; }
    .step-num { flex:0 0 30px; width:30px;height:30px;border-radius:10px;display:grid;place-items:center;background:#251326;color:#ff73bd;font:500 .8rem 'DM Mono',monospace;border:1px solid #5d2850; }
    .step-name { font-weight:700; font-size:.9rem; }
    .step-desc { color:#a69aaa; font-size:.78rem; margin-top:3px; }
    .status { margin-left:auto; white-space:nowrap; font:500 .7rem 'DM Mono',monospace; color:#ff73bd; }
    .status.done { color:#55e6b0; }
    .status.running { color:#ffc36a; }
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] { background:#0d0a11 !important; color:#fff !important; border-color:#453046 !important; border-radius:12px !important; }
    .stTextArea textarea:focus, .stTextInput input:focus { border-color:#ff4db8 !important; box-shadow:0 0 0 1px #ff4db8 !important; }
    div.stButton > button[kind="primary"], .stDownloadButton button { border:0; color:white; font-weight:800; border-radius:13px; min-height:3.15rem;
      background:linear-gradient(100deg,#ff4cae,#ff1688 60%,#b84cff); box-shadow:0 7px 28px rgba(255,46,147,.22); transition:transform .2s,filter .2s; }
    div.stButton > button[kind="primary"]:hover, .stDownloadButton button:hover { filter:brightness(1.12); transform:translateY(-2px); }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #302432; }
    .stTabs [data-baseweb="tab"] { color:#bcaec2; background:#100d14; border-radius:10px 10px 0 0; padding:10px 16px; }
    .stTabs [aria-selected="true"] { color:#ff73bd !important; border-bottom:2px solid #ff2e93 !important; }
    .article { background:#0d0a11; border:1px solid #302432; border-radius:16px; padding:25px; }
    .article h1,.article h2,.article h3 { color:#fff; letter-spacing:-.03em; }
    .article h2 { border-bottom:1px solid #302432; padding-bottom:9px; margin-top:1.7rem; }
    .article p,.article li { color:#d2c7d6; line-height:1.8; }
    .article a { color:#ff73bd; }
    .article blockquote { border-left:3px solid #ff2e93; color:#bcaec2; }
    .stAlert { border-radius:12px; }
    hr { border-color:#302432 !important; }
    footer {visibility:hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand">✦ PINK<span>//</span>PAPER</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted" style="margin:5px 0 24px">AI BLOG STUDIO · GROQ + LANGGRAPH</div>', unsafe_allow_html=True)
    st.markdown("### Workspace")
    page = st.radio("Workspace", ["✦  Create a blog", "▤  My library", "◈  How it works"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<div class="eyebrow">YOUR AI PIPELINE</div>', unsafe_allow_html=True)
    st.markdown("**01**  Route & plan")
    st.markdown("**02**  Research (optional)")
    st.markdown("**03**  Build outline")
    st.markdown("**04**  Write sections")
    st.markdown("**05**  Merge & polish")
    st.markdown("---")
    st.markdown('<div class="small-muted">TEXT GENERATION</div><div style="font-size:1.1rem;font-weight:800;margin-top:6px">⚡ Groq API</div><div class="small-muted">Orchestrated by LangGraph</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:35px;padding:14px;border:1px solid #392238;border-radius:14px;background:#140c16"><div class="eyebrow">DESIGNED FOR CREATORS</div><div style="font-weight:700;margin-top:7px">Ideas in. Great writing out.</div><div class="small-muted" style="margin-top:5px">A visible workflow, not a black box.</div></div>', unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(
    '<div class="hero"><div class="eyebrow">✦ INTELLIGENT WRITING WORKSPACE</div>'
    '<h1>Your next great idea,<br><span class="gradient">beautifully written.</span></h1>'
    '<p>Turn a simple topic into a structured, detailed blog. Watch your LangGraph workflow run, step by step.</p></div>',
    unsafe_allow_html=True,
)

if page.startswith("▤"):
    st.markdown("## Your library")
    files = sorted(OUTPUT_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        st.info("No saved blogs yet. Generate your first article and it will appear here.")
    else:
        for file in files:
            with st.container(border=True):
                c1, c2 = st.columns([5, 1])
                c1.markdown(f"**{file.stem.replace('-', ' ').title()}**")
                c1.caption(f"Updated {time.strftime('%d %b %Y · %H:%M', time.localtime(file.stat().st_mtime))} · {file.stat().st_size:,} bytes")
                c2.download_button("Download", file.read_text(encoding="utf-8"), file_name=file.name, mime="text/markdown", key=f"dl-{file.name}")
    st.stop()

if page.startswith("◈"):
    st.markdown("## How the workflow works")
    st.markdown("Each card below represents a stage in your LangGraph workflow. The live activity panel updates from graph events when the graph streams node updates.")
    descriptions = [
        ("Route & planning", "Decides the writing path and prepares the job."),
        ("Web research", "Optional: gathers external evidence when research is enabled."),
        ("Create blog plan", "Builds an outline so the article has a logical structure."),
        ("Write sections", "Creates the article sections using the configured LLM."),
        ("Merge & finalize", "Combines the sections into the final Markdown article."),
    ]
    for i, (name, desc) in enumerate(descriptions, 1):
        st.markdown(f'<div class="step"><div class="step-num">{i:02}</div><div><div class="step-name">{name}</div><div class="step-desc">{desc}</div></div></div>', unsafe_allow_html=True)
    st.stop()

# ---------- Create view ----------
left, right = st.columns([0.92, 1.08], gap="large")
with left:
    st.markdown('<div class="panel-title"><span class="pink-dot"></span> Compose your article</div>', unsafe_allow_html=True)
    with st.container(border=True):
        topic = st.text_area("BLOG TOPIC", value=st.session_state.get("topic_input", ""), placeholder="e.g. How AI agents are changing software development…", height=110, max_chars=300, label_visibility="visible")
        c1, c2 = st.columns(2)
        with c1:
            writing_style = st.selectbox("WRITING STYLE", ["Detailed & Technical", "Beginner Friendly", "Professional", "SEO Optimized", "Conversational"])
        with c2:
            word_target = st.selectbox("ARTICLE LENGTH", ["Short · 800 words", "Standard · 1,500 words", "Deep dive · 2,500 words"])
        enable_research = st.toggle("Enable web research", value=False, help="Use this if your graph supports the open_book/research path.")
        recency_days = st.number_input("Research recency (days)", min_value=1, max_value=3650, value=365, disabled=not enable_research)
        st.caption("Images are disabled. This workspace focuses on text generation through your configured Groq model.")
        generate = st.button("✦  GENERATE MY BLOG", type="primary", use_container_width=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="panel-title"><span class="pink-dot"></span> Live workflow monitor</div>', unsafe_allow_html=True)
    status_box = st.container(border=True)
    if not generate:
        with status_box:
            steps = [
                ("Route & planning", "Selects the right writing path", "READY"),
                ("Web research", "Collects supporting evidence if enabled", "OPTIONAL"),
                ("Create blog plan", "Builds a coherent article outline", "READY"),
                ("Write sections", "Drafts article sections through the LLM", "READY"),
                ("Merge & finalize", "Assembles the finished Markdown", "READY"),
            ]
            for i, (name, desc, status) in enumerate(steps, 1):
                st.markdown(f'<div class="step"><div class="step-num">{i:02}</div><div style="flex:1"><div class="step-name">{name}</div><div class="step-desc">{desc}</div></div><div class="status">{status}</div></div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel-title"><span class="pink-dot"></span> Article studio <span class="small-muted">/ live preview</span></div>', unsafe_allow_html=True)
    if st.session_state.get("generated_blog"):
        blog = st.session_state["generated_blog"]
        meta = st.session_state.get("blog_meta", {})
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric"><div class="metric-label">Word count</div><div class="metric-value">{len(blog.split()):,}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric"><div class="metric-label">Workflow events</div><div class="metric-value">{meta.get("events", 0)}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric"><div class="metric-label">Duration</div><div class="metric-value">{meta.get("duration", 0):.1f}<span>s</span></div></div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["✦  Preview", "{" + "}  Markdown", "◈  Run details"])
        with tab1:
            st.markdown('<div class="article">', unsafe_allow_html=True)
            st.markdown(blog)
            st.markdown("</div>", unsafe_allow_html=True)
        with tab2:
            st.code(blog, language="markdown", line_numbers=False)
        with tab3:
            st.markdown("**Observed graph events**")
            for event in meta.get("event_log", []):
                st.markdown(f"- `{event}`")
            st.caption("Event labels are derived from the nodes emitted by your LangGraph stream.")
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", topic.strip()).strip("-").lower()[:80] or "generated-blog"
        st.download_button("↓  DOWNLOAD MARKDOWN", blog, file_name=f"{slug}.md", mime="text/markdown", use_container_width=True)
    else:
        st.markdown(
            '<div class="panel" style="min-height:390px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">'
            '<div style="font-size:3.3rem;color:#ff4db8;text-shadow:0 0 28px #ff168866">✧</div>'
            '<div style="font-size:1.35rem;font-weight:800;margin-top:10px">Your canvas is waiting.</div>'
            '<div class="small-muted" style="max-width:330px;margin-top:8px">Enter a topic and generate your article. Your finished blog will appear here with Markdown preview and download options.</div>'
            '<div style="display:flex;gap:8px;margin-top:24px;flex-wrap:wrap;justify-content:center">'
            '<span style="border:1px solid #392238;border-radius:99px;padding:6px 11px;color:#ff86c5;font-size:.75rem">✦ LangGraph</span>'
            '<span style="border:1px solid #392238;border-radius:99px;padding:6px 11px;color:#ff86c5;font-size:.75rem">⚡ Groq</span>'
            '<span style="border:1px solid #392238;border-radius:99px;padding:6px 11px;color:#ff86c5;font-size:.75rem">♡ Markdown</span></div></div>',
            unsafe_allow_html=True,
        )

# ---------- Execute graph with real node-event visualization ----------
if generate:
    if not topic.strip():
        st.warning("Enter a blog topic first.")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        started = time.time()
        event_log = []
        progress_area = st.empty()
        progress_bar = st.progress(0, text="Preparing your writing workflow…")
        event_container = st.container(border=True)
        initial_state = {
            "topic": topic.strip(),
            "mode": "open_book" if enable_research else "closed_book",
            "needs_research": bool(enable_research),
            "queries": [],
            "evidence": [],
            "plan": None,
            "as_of": date.today().isoformat(),
            "recency_days": int(recency_days) if enable_research else 3650,
            "sections": [],
            "merged_md": "",
            "final": "",
        }
        # These are visual milestones only; actual node names are recorded from the graph stream.
        stage_aliases = {
            "route": "Route & planning", "plan": "Create blog plan", "research": "Web research",
            "section": "Write sections", "write": "Write sections", "merge": "Merge & finalize",
            "final": "Merge & finalize", "image": "Image generation (disabled)",
        }
        final_state = {}
        try:
            with st.spinner("LangGraph is running…"):
                # update stream lets the UI display the actual node updates as the graph runs.
                stream = blog_graph.stream(initial_state, stream_mode="updates")
                for update in stream:
                    if isinstance(update, dict):
                        for node_name, payload in update.items():
                            node_label = str(node_name).replace("_", " ").strip().title()
                            lowered = str(node_name).lower()
                            display_name = next((label for key, label in stage_aliases.items() if key in lowered), node_label)
                            event_log.append(node_label)
                            if isinstance(payload, dict):
                                final_state.update(payload)
                            pct = min(95, int(len(event_log) / max(5, len(event_log) + 1) * 100))
                            progress_bar.progress(pct, text=f"Running: {display_name}…")
                            with event_container:
                                st.markdown(f'<div class="step"><div class="step-num">{len(event_log):02}</div><div style="flex:1"><div class="step-name">{display_name}</div><div class="step-desc">LangGraph node emitted an update: <code>{node_label}</code></div></div><div class="status running">RUNNING</div></div>', unsafe_allow_html=True)
                # Some graphs stream partial state only; invoke is not repeated to avoid duplicate generation.
            # If graph stream ends, the last node update payload should contain final fields.
            blog = final_state.get("final") or final_state.get("merged_md")
            if not blog:
                # Try a full invoke only if the stream yielded no final content. This can regenerate, but avoids blank UI.
                result = blog_graph.invoke(initial_state)
                blog = result.get("final") or result.get("merged_md")
                final_state.update(result)
            if not blog:
                raise RuntimeError("The graph finished but returned no 'final' or 'merged_md' content. Check the graph's final node and State keys.")
            elapsed = time.time() - started
            slug = re.sub(r"[^a-zA-Z0-9]+", "-", topic.strip()).strip("-").lower()[:80] or "generated-blog"
            out_file = OUTPUT_DIR / f"{slug}.md"
            out_file.write_text(blog, encoding="utf-8")
            st.session_state["generated_blog"] = blog
            st.session_state["topic_input"] = topic
            st.session_state["blog_meta"] = {"events": len(event_log), "duration": elapsed, "event_log": event_log}
            progress_bar.progress(100, text="Blog generated successfully.")
            st.success(f"Your article is ready — saved to {out_file.as_posix()}")
            st.rerun()
        except Exception as exc:
            progress_bar.empty()
            st.error("The graph hit an error. The details below will help you debug the exact node.")
            st.exception(exc)
            st.info("If this error mentions an image node or forced tool calling, the backend graph still contains image-generation logic. The frontend does not generate images.")
