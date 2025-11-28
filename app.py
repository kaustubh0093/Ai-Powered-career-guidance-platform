import os
from typing import Dict, Optional, List, Tuple

import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool
from langchain.agents import initialize_agent, AgentType

# Output cleaning helper for all model/agent outputs
def as_markdown(output):
    val = getattr(output, "content", None)
    if val is None:
        val = str(output)
    if val.startswith("content='") or val.startswith('content="'):
        start = val.find("'") + 1 if "'" in val else val.find('"') + 1
        val = val[start:]
        if val.endswith("'") or val.endswith('"'):
            val = val[:-1]
    val = val.replace("\\n", "\n").replace("\r", "")
    while "\n\n\n" in val:
        val = val.replace("\n\n\n", "\n\n")
    return val.strip()

# Optional callback for streamed UI (depends on LangChain version)
try:
    from langchain_community.callbacks import StreamlitCallbackHandler
    HAVE_STREAMLIT_CALLBACK = True
except Exception:
    HAVE_STREAMLIT_CALLBACK = False

load_dotenv()

st.set_page_config(
    page_title="🎯 AI Career Guidance Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

CAREER_CATEGORIES = {
    "💻 Technology": [
        "AI & Machine Learning Engineer",
        "Data Scientist",
        "Cybersecurity Analyst",
        "Cloud Solutions Architect",
        "Full Stack Developer",
        "DevOps Engineer",
        "Blockchain Developer",
        "Mobile App Developer",
        "Data Engineer",
        "Software Quality Assurance Engineer",
    ],
    "🩺 Healthcare": [
        "Medical Data Analyst",
        "Telehealth Specialist",
        "Biomedical Engineer",
        "Clinical Research Associate",
        "Healthcare Administrator",
        "Public Health Specialist",
        "Medical Laboratory Technologist",
        "Physiotherapist",
        "Pharmacy Manager",
        "Healthcare IT Consultant",
    ],
    "💼 Business": [
        "Business Analyst",
        "Digital Marketing Strategist",
        "Financial Data Analyst",
        "Product Manager",
        "HR Analytics Specialist",
        "Management Consultant",
        "Supply Chain Analyst",
        "Investment Banker",
        "Brand Manager",
        "Operations Manager",
    ],
    "🎥 Content Creation": [
        "Video Content Strategist",
        "Social Media Manager",
        "Copywriter / Content Writer",
        "Graphic Designer",
        "SEO Specialist",
        "Podcast Producer",
        "UX/UI Designer",
        "Video Editor",
        "Influencer Marketing Manager",
        "Content Marketing Strategist",
    ],
}

def load_api_keys() -> Dict[str, Optional[str]]:
    google_api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    serpapi_key = os.getenv("SERPAPI_API_KEY") or st.secrets.get("SERPAPI_API_KEY", "")
    return {"google_api_key": google_api_key, "serpapi_key": serpapi_key}

def initialize_session_state():
    defaults = {
        "chat_history": [],
        "chat_messages": [],
        "career_insights": None,
        "market_analysis": None,
        "college_recommendations": None,
        "resume_feedback": None,
        "selected_career": None,
        "api_keys_validated": False,
        "active_tab": "career_insights",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

@st.cache_resource
def initialize_llm_and_tools(google_api_key: str, serpapi_key: str) -> Tuple[Optional[ChatGoogleGenerativeAI], Optional[List[Tool]]]:
    try:
        if not google_api_key:
            raise ValueError("Google API key is required.")
        if not serpapi_key:
            raise ValueError("SerpAPI key is required.")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.7,
            convert_system_message_to_human=True,
        )

        search = SerpAPIWrapper(
            serpapi_api_key=serpapi_key,
            params={"engine": "google", "google_domain": "google.com", "gl": "in", "hl": "en"},
        )

        search_tool = Tool(
            name="web_search",
            description="Use to search the web for job market trends, salaries, companies, Indian colleges, and live data.",
            func=search.run,
        )

        return llm, [search_tool]
    except Exception as e:
        st.error(f"❌ Error initializing LLM/tools: {e}")
        return None, None

def create_agent_with_tools(llm, tools: List[Tool]):
    try:
        agent_executor = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )
        return agent_executor
    except Exception as e:
        st.error(f"❌ Error creating agent: {e}")
        return None

def generate_career_insights(category: str, subcareer: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        career_prompt = f"""
Generate a comprehensive career analysis for:

**Category**: {category}
**Career**: {subcareer}

Provide structured markdown that includes:
1) Career Overview (role, responsibilities, daily tasks)
2) Required Skills & Tools (technical + soft skills)
3) Learning Roadmap (beginner → intermediate → advanced)
4) Career Progression Path (roles & salary bands in India)
5) Future Outlook & trends
6) Suggested Resources (courses, books, certifications)
7) Quick Reference Summary (salary ranges in INR, demand in India, remote options)

Keep the output practical, actionable, and formatted in markdown. Focus on the Indian job market context.
"""

        with st.spinner("🧭 Generating career insights..."):
            output = llm.invoke(career_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating career insights: {e}")
        return f"❌ Unable to generate career insights. Error: {e}"

def generate_market_analysis(subcareer: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        market_prompt = f"""
Search the web (live) and analyze the current job market in India for the role: "{subcareer}".

Please include:
- Current job demand and hiring trends in India (last 12 months)
- Typical salary ranges in INR (entry / mid / senior level)
- Top Indian companies hiring and industry sectors
- Major hiring cities in India (Bangalore, Mumbai, Delhi, Hyderabad, Pune, etc.)
- Skills in highest demand for this role in India
- Remote work availability and trends in India
- Short list of sources (urls or site names) used

Return a concise, well-structured markdown analysis with bullet points and a small summary table.
Focus specifically on the Indian job market.
"""

        with st.spinner("📊 Fetching live market data..."):
            output = llm.invoke(market_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating market analysis: {e}")
        return f"❌ Unable to fetch market analysis. Error: {e}"

def generate_college_recommendations(subcareer: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        college_prompt = f"""
As a college advisor, provide detailed recommendations for pursuing a career in "{subcareer}" in India.

Please include:

1) **Recommended Educational Paths**:
   - Degree programs (BTech, BSc, BA, MBA, MSc, etc.)
   - Specializations to focus on
   - Duration and typical eligibility

2) **Top Indian Colleges/Universities** (at least 10-15):
   - IITs, NITs, IIITs, and other premier institutes
   - State universities and private colleges
   - Include admission processes (JEE, GATE, CAT, etc.)
   - Approximate fees and placement records where known

3) **Alternative Education Paths**:
   - Online courses and certifications
   - Bootcamps and vocational training
   - Diploma programs

4) **Entrance Exams**:
   - Required entrance exams for admission
   - Preparation tips and resources

5) **Scholarships & Financial Aid**:
   - Government scholarships available
   - Merit-based and need-based options

6) **Additional Tips**:
   - Best states/cities for education in this field
   - Industry certifications to pursue alongside degree
   - Internship opportunities during education

Format the response in clear markdown with sections, bullet points, and tables where appropriate.
Focus exclusively on Indian institutions and the Indian education system.
"""

        with st.spinner("🎓 Generating college recommendations..."):
            output = llm.invoke(college_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating college recommendations: {e}")
        return f"❌ Unable to generate college recommendations. Error: {e}"

def generate_resume_feedback(resume_text: str, target_role: str, llm: ChatGoogleGenerativeAI) -> str:
    try:
        if llm is None:
            raise RuntimeError("LLM not initialized")

        resume_prompt = f"""
As an expert resume coach, analyze the following resume for the target role: "{target_role}"

**Resume Content**:
{resume_text}

Provide comprehensive feedback in the following structure:

1) **Overall Assessment** (Score: X/10):
   - Brief summary of strengths and weaknesses
   - First impression rating

2) **Content Analysis**:
   - Relevance to target role
   - Key achievements and quantifiable results
   - Skills alignment with job requirements
   - Missing critical information

3) **Format & Structure**:
   - Layout and readability assessment
   - Section organization
   - Length appropriateness

4) **Specific Improvements Needed**:
   - What to add (skills, experiences, keywords)
   - What to remove or reduce
   - How to rephrase key sections
   - ATS (Applicant Tracking System) optimization tips

5) **Section-by-Section Feedback**:
   - Summary/Objective
   - Work Experience
   - Education
   - Skills
   - Projects/Certifications

6) **Action Items** (Priority-ordered):
   - Top 5-7 changes to make immediately
   - Keywords to include for ATS
   - Formatting improvements

7) **Example Improvements**:
   - Before/After examples for 2-3 bullet points
   - Better ways to phrase achievements

8) **Industry-Specific Tips**:
   - Tailored advice for the Indian job market
   - Cultural considerations for Indian recruiters

Be constructive, specific, and actionable. Use markdown formatting with clear sections.
"""

        with st.spinner("📝 Analyzing resume..."):
            output = llm.invoke(resume_prompt)

        return output

    except Exception as e:
        st.error(f"❌ Error generating resume feedback: {e}")
        return f"❌ Unable to analyze resume. Error: {e}"

def create_chat_interface(agent_executor):
    st.subheader("💬 AI Career Assistant")
    st.markdown("Ask anything about careers, skills, pathways, colleges, resumes, or the job market.")

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your career question here..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        context_preview = "\n".join(
            f"{m['role']}: {m['content']}" for m in st.session_state.chat_messages[-8:]
        )
        chat_prompt = f"""You are a helpful AI career advisor with expertise in:
- Career guidance and job market trends (especially in India)
- Indian colleges and universities
- Resume writing and optimization
- Skills development and learning paths

Conversation context:
{context_preview}

User question: {prompt}

Provide a helpful, concise answer. If you need live data about Indian colleges, job markets, or current trends, use the web_search tool.
When discussing education, focus on Indian institutions. When discussing salaries, use INR.
"""

        with st.chat_message("assistant"):
            try:
                if HAVE_STREAMLIT_CALLBACK:
                    container = st.container()
                    cb = StreamlitCallbackHandler(parent_container=container)
                    response = agent_executor.run(chat_prompt, callbacks=[cb])
                else:
                    response = agent_executor.run(chat_prompt)
                st.markdown(as_markdown(response))
                st.session_state.chat_messages.append({"role": "assistant", "content": as_markdown(response)})
            except Exception as e:
                err = f"❌ Error while answering: {e}"
                st.error(err)
                st.session_state.chat_messages.append({"role": "assistant", "content": err})

def main():
    initialize_session_state()

    st.title("🎯 AI-Powered Career Guidance Platform")
    st.markdown(
        """
    **Discover your ideal career path with AI-powered insights, college recommendations, resume coaching, and real-time market analysis.**
    *Powered by Google Gemini, LangChain Agents, and SerpAPI | Focused on Indian Job Market & Education*
    """
    )

    api_keys = load_api_keys()
    with st.sidebar:
        st.header("🔧 Configuration")
        google_key = st.text_input(
            "🤖 Google Gemini API Key", value=api_keys["google_api_key"], type="password"
        )
        serpapi_key = st.text_input(
            "🔍 SerpAPI Key", value=api_keys["serpapi_key"], type="password"
        )

        if google_key and serpapi_key:
            st.success("✅ API keys configured")
            st.session_state.api_keys_validated = True
        else:
            st.warning("⚠️ Provide both API keys to enable live features")
            st.session_state.api_keys_validated = False

        st.markdown("---")
        st.markdown(
            """
        **How to use**
        1. Configure API keys above (or set in .env / Streamlit secrets)
        2. Choose career category & role
        3. Use tabs to explore:
           - 🧭 Career Insights
           - 📊 Market Analysis
           - 🎓 College Advisor
           - 📝 Resume Coach
        4. Use chat for personalized questions
        """
        )

        if st.button("🔄 Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if not st.session_state.api_keys_validated:
        st.info("👈 Please provide your Google Gemini and SerpAPI keys in the sidebar to get started.")
        st.subheader("🌟 Features")
        st.markdown(
            """
- 📊 Role analysis & learning roadmap
- 📈 Live market analysis (Indian job market)
- 🎓 College recommendations (Indian institutions)
- 📝 AI-powered resume coaching
- 💬 Interactive career advisor chat
- 🏢 Multi-industry coverage (Tech, Healthcare, Business, Content)
"""
        )
        return

    llm, tools = initialize_llm_and_tools(google_key, serpapi_key)
    if not llm or not tools:
        st.error("❌ Failed to initialize AI components. Check your API keys and network.")
        return

    agent_executor = create_agent_with_tools(llm, tools)
    if agent_executor is None:
        st.error("❌ Agent initialization failed.")
        return

    st.subheader("🎯 Select Your Career Interest")
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_category = st.selectbox("📁 Choose a career category:", list(CAREER_CATEGORIES.keys()))
    with col2:
        selected_subcareer = st.selectbox("🎯 Choose specific career:", CAREER_CATEGORIES[selected_category])

    # Tab interface for different features
    tab1, tab2, tab3, tab4 = st.tabs(["🧭 Career Insights", "📊 Market Analysis", "🎓 College Advisor", "📝 Resume Coach"])

    with tab1:
        st.markdown("### 🧭 Career Insights & Learning Roadmap")
        if st.button("🚀 Generate Career Insights", key="btn_career_insights", use_container_width=True):
            st.session_state.selected_career = f"{selected_category} → {selected_subcareer}"
            career_insights = generate_career_insights(selected_category, selected_subcareer, llm)
            st.session_state.career_insights = career_insights
            st.markdown(as_markdown(career_insights))
        elif st.session_state.career_insights:
            st.info(f"📋 Showing cached results for: **{st.session_state.selected_career}**")
            st.markdown(as_markdown(st.session_state.career_insights))

    with tab2:
        st.markdown("### 📊 Live Market Analysis")
        if st.button("📈 Fetch Market Data", key="btn_market_analysis", use_container_width=True):
            st.session_state.selected_career = f"{selected_category} → {selected_subcareer}"
            market_analysis = generate_market_analysis(selected_subcareer, llm)
            st.session_state.market_analysis = market_analysis
            st.markdown(as_markdown(market_analysis))
        elif st.session_state.market_analysis:
            st.info(f"📋 Showing cached results for: **{st.session_state.selected_career}**")
            st.markdown(as_markdown(st.session_state.market_analysis))

    with tab3:
        st.markdown("### 🎓 College & University Recommendations")
        st.markdown("*Get personalized recommendations for Indian colleges and universities*")
        if st.button("🏛️ Get College Recommendations", key="btn_college_recs", use_container_width=True):
            st.session_state.selected_career = f"{selected_category} → {selected_subcareer}"
            college_recommendations = generate_college_recommendations(selected_subcareer, llm)
            st.session_state.college_recommendations = college_recommendations
            st.markdown(as_markdown(college_recommendations))
        elif st.session_state.college_recommendations:
            st.info(f"📋 Showing cached results for: **{st.session_state.selected_career}**")
            st.markdown(as_markdown(st.session_state.college_recommendations))

    with tab4:
        st.markdown("### 📝 Resume Coach & Feedback")
        st.markdown("*Get AI-powered feedback on your resume*")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["📄 Upload Resume File", "✍️ Paste Resume Text"],
            horizontal=True,
            key="resume_input_method"
        )
        
        resume_text = ""
        
        if input_method == "📄 Upload Resume File":
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF, DOCX, or TXT)",
                type=["pdf", "docx", "doc", "txt"],
                key="resume_file_uploader",
                help="Supported formats: PDF, Word (DOCX/DOC), and plain text files"
            )
            
            if uploaded_file is not None:
                try:
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    
                    if file_extension == 'txt':
                        resume_text = uploaded_file.read().decode('utf-8')
                        st.success(f"✅ Loaded {len(resume_text)} characters from {uploaded_file.name}")
                    
                    elif file_extension == 'pdf':
                        try:
                            import PyPDF2
                            from io import BytesIO
                            
                            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                            resume_text = ""
                            for page in pdf_reader.pages:
                                resume_text += page.extract_text() + "\n"
                            st.success(f"✅ Extracted {len(resume_text)} characters from PDF")
                        except ImportError:
                            st.error("❌ PyPDF2 not installed. Install it with: pip install PyPDF2")
                        except Exception as e:
                            st.error(f"❌ Error reading PDF: {e}")
                    
                    elif file_extension in ['docx', 'doc']:
                        try:
                            import docx
                            from io import BytesIO
                            
                            doc = docx.Document(BytesIO(uploaded_file.read()))
                            resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                            st.success(f"✅ Extracted {len(resume_text)} characters from Word document")
                        except ImportError:
                            st.error("❌ python-docx not installed. Install it with: pip install python-docx")
                        except Exception as e:
                            st.error(f"❌ Error reading Word document: {e}")
                    
                    # Show preview
                    if resume_text:
                        with st.expander("📄 Preview extracted text"):
                            st.text_area("Resume content:", resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=200, disabled=True)
                            
                except Exception as e:
                    st.error(f"❌ Error processing file: {e}")
        
        else:  # Paste text option
            resume_text = st.text_area(
                "Paste your resume content here:",
                height=300,
                placeholder="Copy and paste your resume text here...\n\nInclude all sections: Summary, Experience, Education, Skills, etc.",
                key="resume_text_input"
            )
        
        target_role_input = st.text_input(
            "Target Role (optional - uses selected career if empty):",
            placeholder="e.g., Senior Data Scientist",
            key="target_role_input"
        )
        
        if st.button("🔍 Analyze Resume", key="btn_resume_analysis", use_container_width=True):
            if not resume_text or len(resume_text.strip()) < 100:
                st.warning("⚠️ Please provide your resume content (at least 100 characters)")
            else:
                target_role = target_role_input if target_role_input else selected_subcareer
                resume_feedback = generate_resume_feedback(resume_text, target_role, llm)
                st.session_state.resume_feedback = resume_feedback
                st.markdown(as_markdown(resume_feedback))
        elif st.session_state.resume_feedback:
            st.info("📋 Showing previous resume analysis")
            st.markdown(as_markdown(st.session_state.resume_feedback))

    st.markdown("---")
    create_chat_interface(agent_executor)

    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666; padding: 16px;'>
        🎯 <strong>AI-Powered Career Guidance Platform</strong> — Built with LangChain & Gemini | 🇮🇳 Indian Market Focus
    </div>
    """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()