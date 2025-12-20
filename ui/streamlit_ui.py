import streamlit as st
from models.cv_model import CVAnalysis
from services.pdf_processor import PDFTextExtractor
from services.cv_evaluator import CVEvaluator

def main():
    """Main function that defines the Streamlit user interface"""
    
    st.set_page_config(
        page_title="CV Evaluation System",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📄 AI-powered CV evaluation system")
    st.markdown("""
    **Analyze CVs and evaluate candidates objectively using AI**
    
    This system uses artificial intelligence to:
    - Extract key information from PDF resumes
    - Analyze candidate experience and skills
    - Evaluate fit for specific positions
    - Provide objective hiring recommendations
    """)
    
    st.divider()
    
    col_enter, col_result = st.columns([1, 1], gap="large")
    
    with col_enter:
        process_input()
    
    with col_result:
        show_results_area()

def process_input():
    """Handles user data input"""
    
    st.header("📋 Input Data")
    
    file_cv = st.file_uploader(
        "**1. Upload the candidate's CV (PDF)**",
        type=['pdf'],
        help="Select a PDF file containing the resume to be evaluated. Make sure the text is legible and not in image format."
    )
    
    if file_cv is not None:
        st.success(f"✅ File uploaded: {file_cv.name}")
        st.info(f"📊 Size: {file_cv.size:,} bytes")
    
    st.markdown("---")
    
    st.markdown("**2. Job description**")
    job_description = st.text_area(
        "Detail the requirements, responsibilities, and skills needed:",
        height=250,
        placeholder="""Detailed example:

**Position:** Senior Frontend Developer

**Required Qualifications:**
- 3+ years of frontend development experience
- Proficiency in React.js and JavaScript/TypeScript
- Experience with HTML5, CSS3, and CSS frameworks (Bootstrap, Tailwind)
- Knowledge of build tools (Webpack, Vite)

**Desired Qualifications:**
- Experience with Next.js or similar tools
- Knowledge of testing (Jest, Cypress)
- Familiarity with Agile methodologies
- Intermediate to advanced English

**Responsibilities:**
- Development of responsive user interfaces
- Collaboration with design and backend teams
- Optimization of web application performance
- Maintenance of legacy code""",
        help="Be specific about technical requirements, required experience, and job responsibilities."
    )
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        analyze = st.button(
            "🔍 Analyze Candidate", 
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        if st.button("🗑️ Clean", use_container_width=True):
            st.rerun()
    
    st.session_state['file_cv'] = file_cv
    st.session_state['job_description'] = job_description
    st.session_state['analyze'] = analyze

def show_results_area():
    """Displays the analysis results area"""
    
    st.header("📊 Analysis Result")
    
    if st.session_state.get('analyze', False):
        file_cv = st.session_state.get('file_cv')
        job_description = st.session_state.get('job_description', '').strip()
        
        if file_cv is None:
            st.error("⚠️ Please upload a PDF file with your resume.")
            return
            
        if not job_description:
            st.error("⚠️ Please provide a detailed job description")
            return
        
        process_analysis(file_cv, job_description)
    else:
        st.info("""
        👆 **Instructions:**
        
        1. Upload a CV in PDF format in the left column.
        2. Describe the job in detail.
        3. Click on "Analyze Candidate."
        4. The complete candidate analysis will appear here.
        
        **Tips for better results:**
        - Use CVs with selectable text (not scanned images).
        - Be specific in the job description.
        - Include both required and desired qualifications.
        """)

def process_analysis(file_cv, job_description):
    """Process the complete CV analysis"""
    
    with st.spinner("🔄 processing resume..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📄 Extracting text from the PDF...")
        progress_bar.progress(25)
        
        pdf_extractor = PDFTextExtractor()
        text_cv = pdf_extractor.extract_text_df(file_cv)
        
        if text_cv.startswith("Error"):
            st.error(f"❌ {text_cv}")
            return
        
        status_text.text("🤖 Preparing AI analysis...")
        progress_bar.progress(50)
        
        status_text.text("📊 Analyzing candidate...")
        progress_bar.progress(75)
        
        cv_evaluator = CVEvaluator()
        result = cv_evaluator.evaluate_candidate(text_cv, job_description)
        
        status_text.text("✅ Analysis completed")
        progress_bar.progress(100)
        
        progress_bar.empty()
        status_text.empty()
        
        show_results(result)

def show_results(result: CVAnalysis):
    """It presents the analysis results in a structured and professional manner."""
    
    st.subheader("🎯 Main Assessment")
    
    if result.adjustment_percentage >= 80:
        color = "🟢"
        level = "STRONG"
        menssage = "Highly recommended candidate"
    elif result.adjustment_percentage >= 60:
        color = "🟡"
        level = "SUITABLE"
        menssage = "Recommended candidate with reservations"
    elif result.adjustment_percentage >= 40:
        color = "🟠"
        level = "MARGINAL"
        menssage = "Candidate requires further evaluation"
    else:
        color = "🔴"
        level = "WEAK"
        menssage = "Not recommended candidate"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Percentage of Fit to Position",
            value=f"{result.adjustment_percentage}%",
            delta=f"{color} {level}"
        )
        st.markdown(f"**{menssage}**")
    
    st.divider()
    
    st.subheader("👤 Candidate Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**👨‍💼 Name:** {result.candidate_name}")
        st.info(f"**⏱️ Experience:** {result.years_experience} years")
    
    with col2:
        st.info(f"**🎓 Education:** {result.education}")
    
    st.subheader("💼 Relevant Experience")
    st.info(f"📋 **Experience summary:**\n\n{result.relevant_experience}")
    
    st.divider()
    
    st.subheader("🛠️ Key Technical Skills")
    if result.key_skills:
        cols = st.columns(min(len(result.key_skills), 4))
        for i, skill in enumerate(result.key_skills):
            with cols[i % 4]:
                st.success(f"✅ {skill}")
    else:
        st.warning("No specific technical skills were identified.")
    
    st.divider()
    
    col_strengths, col_improvements = st.columns(2)
    
    with col_strengths:
        st.subheader("💪 Main Strengths")
        if result.strenghts:
            for i, strength in enumerate(result.strenghts, 1):
                st.markdown(f"**{i}.** {strength}")
        else:
            st.info("No specific strengths were identified")
    
    with col_improvements:
        st.subheader("📈 Development Areas")
        if result.improvement_areas:
            for i, area in enumerate(result.improvement_areas, 1):
                st.markdown(f"**{i}.** {area}")
        else:
            st.info("No specific areas for improvement were identified")
    
    st.divider()
    
    st.subheader("📋 Final Recommendation")
    
    if result.adjustment_percentage >= 70:
        st.success("""
        ✅ **RECOMMENDED CANDIDATE**
        
        The candidate's profile is well aligned with the job requirements.
        It is recommended to proceed with the next stages of the selection process.
        """)
    elif result.adjustment_percentage >= 50:
        st.warning("""
        ⚠️ **CANDIDATE WITH POTENTIAL**
        
        The candidate shows potential but requires further evaluation.
        A technical interview is recommended to validate specific skills.
        """)
    else:
        st.error("""
        ❌ **CANDIDATE NOT RECOMMENDED**
        
        The candidate's profile does not sufficiently match the job requirements.
        We recommend continuing the search for more suitable candidates.
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save Analysis", use_container_width=True):
            st.info("Saving functionality - Under development")