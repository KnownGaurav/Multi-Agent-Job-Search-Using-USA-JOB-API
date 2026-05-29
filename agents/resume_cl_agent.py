from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=GEMINI_API_KEY
)

def get_resume_cl_agent():
    return Agent(
        # FIX: Fixed typo "Copver" to "Cover"
        role="Resume and Cover Letter Writer",
        goal="Customize application materials for specific job descriptions",
        backstory="You're an expert in professional writing and tailoring resumes for job applications, especially in government and tech roles.",
        llm=llm,
        verbose=True
    )

def create_resume_cl_task(agent, job_summary, resume):
    return Task(
        description=f"""
        Based on the job summary and the provided resume, create a tailored resume and cover letter that highlights the most relevant skills and experiences for the job.

        Job Summary: {job_summary}
        Resume: {resume}

        Your output should include:
        1. Updated professional summary for the resume.
        2. A personalized cover letter suitable for a government job application.
        """,
        agent=agent,
        expected_output="""
        <<RESUME_SUMMARY>>
        [Your tailored 3-5 sentence resume summary here]

        <<COVER_LETTER>>
        [Your personalized cover letter here]
        """, 
        output_file='data/resume_agent_output.txt'
    )