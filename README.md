# Multi-Agent Job Search Assistant 🚀
An intelligent, automated system powered by **CrewAI** and **LangChain** that streamlines the job search workflow by analyzing job descriptions (using the USAJOBS API or custom inputs) and tailoring professional bio/resume data to match role requirements.

Built with a slick **Streamlit** user interface and backed by Google's powerful **Gemini** models.

---

## 🛠️ Project Architecture
This application utilizes a multi-agent orchestrated pipeline. Instead of a single prompt trying to do everything, specialized agents tackle isolated tasks sequentially to minimize hallucinations and maximize accuracy:

1. **Job Description (JD) Analyst Agent:** Extracts core competencies, required technical skills, and key responsibilities from target job openings.
2. **Resume Matcher / Orchestrator Agent:** Cross-references the extracted requirements against your personal background and automatically identifies gaps, strengths, and alignment strategies.

---

## 🚀 Features
* **Multi-Agent Orchestration:** Driven by `crewai` workflows to deliver deep, structured analysis.
* **LLM Powered:** Leverages `langchain-google-genai` (Gemini 1.5 Pro/Flash) for high-context comprehension.
* **Interactive UI:** A crisp `Streamlit` dashboard for entering job details, pasting resumes, and monitoring execution in real-time.
* **Robust Error Handling:** Pre-configured to bypass typical Pydantic type-mismatch validation errors common in framework integrations.

---

## 📁 Directory Structure
```text
├── agents/
│   ├── __init__.py
│   └── jd_analyst.py       # Defines specific CrewAI agents and their roles
├── orchestrator.py         # Sets up the Crew, tasks, and sequential pipeline
├── streamlit.py            # Streamlit frontend UI app entry point
├── .gitignore              # Safely ignores venv, .env, and cache files
├── README.md               # Project documentation
└── requirements.txt        # Python project dependencies

