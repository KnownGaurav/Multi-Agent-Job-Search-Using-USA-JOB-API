import streamlit as st
from usajobs_api import fetchusa_jobs
from orchestrator import run_pipeline 

# App Layout Configuration
st.set_page_config(page_title="AI Job Hunt Assistant", page_icon="💼", layout="wide")

st.title("💼 AI Job Hunt Assistant")
st.markdown("""
Welcome to your intelligent, multi-agent agent portal. This tool hooks directly into USAJobs to extract openings, 
deconstruct complex government requirements, align your resume text, and draft professional agency correspondence.
""")

# Setup Sidebar for profile inputs so they remain visible and don't reset
st.sidebar.header("👤 Your Profile Information")
resume_text = st.sidebar.text_area("Paste your original Resume here", height=250, placeholder="Paste plain text resume details...")
user_bio = st.sidebar.text_area("Brief Background Bio", value="Experienced software developer looking to align core engineering milestones with modern public-service missions.", height=100)

# --- STEP 1: FORM FOR SEARCH CRITERIA ---
st.markdown("### 🔍 Step 1: Query Live Federal Database")
with st.form("Job_search_form"):
    col1, col2 = st.columns(2)
    with col1:
        job_keyword = st.text_input("Job Position or Keyword", "Software Engineer")
    with col2:
        location = st.text_input("Target Location Filter", "remote")
        
    submit = st.form_submit_button("Fetch Live Postings")

# Handle Form Execution outside the form container block to guarantee Session State stability
if submit:
    with st.spinner("Establishing secure handshake with USAJobs API..."):
        job_posts = fetchusa_jobs(job_keyword, location, results_per_page=5)
        
        if not job_posts:
            st.error("No job postings found. Please modify your keywords or search filters.")
        else:
            st.session_state['job_posts'] = job_posts
            st.success(f"Successfully synchronized {len(job_posts)} target listings! Make your selection below.")

# --- STEP 2: DISPLAY RESULTS & PROCESSING ---
if "job_posts" in st.session_state and st.session_state['job_posts']:
    st.markdown("---")
    st.markdown("### 📋 Step 2: Target Selection & Agent Pipeline Activation")
    st.info("Check the checkboxes next to the positions you want your AI Crew to build assets for.")
    
    selected_jobs = []
    
    # Render checkboxes using our flattened usajobs_api dictionary format
    for idx, job in enumerate(st.session_state['job_posts']):
        job_title = job.get('title', 'Unknown Position')
        organization = job.get('agency', 'Unknown Agency')
        job_location = job.get('location', 'Remote')
        
        checkbox_label = f"📍 **{job_title}** — *{organization}* ({job_location})"
        
        # If checked, store the clean job dictionary directly into our task pool
        if st.checkbox(checkbox_label, key=f"job_check_{idx}"):
            selected_jobs.append(job)

    st.markdown("### 🚀 Step 3: Initialize Workflow")
    if st.button("Trigger Multi-Agent Production", type="primary"):
        if not selected_jobs:
            st.warning("Please select at least one active job posting to process.")
        elif not resume_text.strip():
            st.error("Missing Profile Asset: Please paste your current resume text into the sidebar dashboard.")
        else:
            # Iterate sequentially through chosen target records
            for job in selected_jobs:
                title = job.get('title', 'Unknown Position')
                agency = job.get('agency', 'Unknown Agency')
                
                # Visual container container for the active task
                with st.expander(f"🔄 Processing Pipeline: {title} at {agency}", expanded=True):
                    with st.spinner("Assembling CrewAI Agent Task-Force..."):
                        
                        # Direct, clean call to our updated pipeline orchestrator
                        result_suite = run_pipeline(job, resume_text, user_bio)
                        
                        st.success(f"Assets generated and backed up for {title}!")
                        st.markdown("#### Generated Application Outputs")
                        st.markdown(result_suite)