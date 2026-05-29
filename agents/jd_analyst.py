from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

# Ensure the API key is passed correctly to LangChain's Google GenAI integration
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    api_key=GEMINI_API_KEY
)

def get_jd_analyst_agent():
    """Defines the specialized Federal Job Description Analyst."""
    return Agent(
        role="Federal Job Description Analyst",
        goal="Deconstruct complex government job postings into distinct, actionable technical competencies and compliance baselines.",
        backstory=(
            "You are an expert HR strategist specializing in USAJOBS federal hiring standards. "
            "You possess deep experience navigating complex government grading scales and structural requirements. "
            "You are skilled at stripping away dense institutional text to find exactly what technical skills, certifications, "
            "and qualifications an applicant needs to pass automated vetting filters."
        ),
        llm=llm,
        verbose=True
    )

def create_jd_analysis_task(agent, job_description):
    """Creates the structural analysis task parsing raw job data into structured fields."""
    return Task(
        description=f"""
        Deconstruct and analyze the following USAJobs federal posting data. 
        Identify the structural responsibilities, specialized core skill requirements, and mandatory compliance qualifications.

        Job Post Context:
        {job_description}
        """,
        expected_output=(
            "A structured markdown report using explicit headers:\n"
            "## 1. Role Core Responsibilities\n"
            "## 2. Mandatory Qualifications & Eligibility\n"
            "## 3. Highly Desired Core Technical Skills"
        ),
        agent=agent
    )