from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

# Setting up LLM configuration with current parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,  # Slightly higher temperature for natural, engaging communication
    api_key=GEMINI_API_KEY
)

def get_messaging_agent():
    """Defines the specialized Professional Outreach and Networking Agent."""
    return Agent(
        role="Professional Outreach Coordinator",
        goal="Craft highly personalized, professional, and high-conversion networking messages for federal hiring pipelines.",
        backstory=(
            "You are an expert corporate communications strategist with extensive experience "
            "navigating public sector networking and agency outreach. You understand the "
            "balance between formal civil service respect and modern professional confidence. "
            "You excel at turning a static biography into a compelling narrative that quickly captures "
            "a hiring authority's attention in under 30 seconds."
        ),
        llm=llm,
        verbose=True
    )

def create_messaging_task(agent, job_summary, agency_name, user_bio):
    """Creates the text task for generating professional outreach correspondence."""
    return Task(
        description=f"""
        Based on the provided parameters, craft a highly concise, polished, and impactful professional message 
        introducing the candidate to a hiring team or agency representative. 

        Ensure the output strictly aligns the candidate's background milestones to the needs of the target position 
        while remaining clear and digestible.

        ---
        Target Agency: {agency_name}
        Job Summary: {job_summary}
        User Biography/Background: {user_bio}
        ---
        """,
        expected_output=(
            "A copy-paste-ready professional outreach message formatted with clear paragraph breaks. "
            "It must include:\n"
            "1. A strong subject line variant.\n"
            "2. A formal, respectful greeting.\n"
            "3. An impact statement matching the user's background directly to the agency's current mission.\n"
            "4. A clear, low-friction call-to-action inviting further communication."
        ),
        agent=agent
    )