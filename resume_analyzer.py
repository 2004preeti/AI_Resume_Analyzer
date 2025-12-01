# import streamlit as st
# import os
# import tempfile
# import PyPDF2
# import google.generativeai as genai
# from PIL import Image
# import io
# import base64
# from io import BytesIO

# # Set page configuration
# st.set_page_config(
#     page_title="AI Resume Analyzer",
#     page_icon="📝",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize session state variables
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
    
# if 'analysis_result' not in st.session_state:
#     st.session_state.analysis_result = ""

# # Initialize additional session state variables
# if 'user_input' not in st.session_state:
#     st.session_state.user_input = ""
# if 'resume_text' not in st.session_state:
#     st.session_state.resume_text = ""
# if 'job_title' not in st.session_state:
#     st.session_state.job_title = ""
# if 'job_description' not in st.session_state:
#     st.session_state.job_description = ""

# # Add custom CSS for better styling
# st.markdown("""
# <style>
#     .main {
#         padding: 2rem;
#     }
#     .stApp {
#     }
#     .stButton button {
#         background-color: #4361ee;
#         color: white;
#         border-radius: 5px;
#         padding: 10px 20px;
#         font-weight: bold;
#         transition: all 0.3s ease;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.15);
#     }
#     .stButton button:hover {
#         background-color: #3a56e4;
#         box-shadow: 0 5px 15px rgba(0,0,0,0.2);
#         transform: translateY(-2px);
#     }
#     .result-container {
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#         border-left: 5px solid #4361ee;
#         margin: 20px 0;
#     }
#     h1, h2, h3 {
#         color: #2C3E50;
#         font-weight: 700;
#     }
#     h1 {
#         background: linear-gradient(90deg, #4361ee, #3a0ca3);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         font-size: 2.5rem;
#     }
#     .highlight {
#         padding: 10px;
#         border-left: 5px solid #4361ee;
#         margin: 10px 0;
#     }
#     .section-header {
#         padding: 10px 15px;
#         border-radius: 5px;
#         margin-bottom: 15px;
#         border-left: 4px solid #4361ee;
#         font-weight: bold;
#     }
#     .chat-user {
#         padding: 12px 15px;
#         border-radius: 15px 15px 15px 0;
#         margin-bottom: 15px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#         position: relative;
#         animation: slideInLeft 0.3s ease;
#     }
#     .chat-ai {
#         padding: 12px 15px;
#         border-radius: 15px 15px 0 15px;
#         margin-bottom: 15px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#         border-left: 3px solid #4361ee;
#         position: relative;
#         animation: slideInRight 0.3s ease;
#     }
#     @keyframes slideInLeft {
#         from { opacity: 0; transform: translateX(-20px); }
#         to { opacity: 1; transform: translateX(0); }
#     }
#     @keyframes slideInRight {
#         from { opacity: 0; transform: translateX(20px); }
#         to { opacity: 1; transform: translateX(0); }
#     }
#     .upload-section, .job-details-section {
#         background-color: white;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#         height: 100%;
#         transition: transform 0.3s ease;
#     }
#     .upload-section:hover, .job-details-section:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 6px 12px rgba(0,0,0,0.1);
#     }
#     /* Custom file uploader */
#     .stFileUploader > div:first-child {
#         width: 100%;
#         border: 2px dashed #4361ee;
#         background-color: rgba(67, 97, 238, 0.05);
#         border-radius: 8px;
#         padding: 25px 0;
#     }
#     .stFileUploader > div:first-child:hover {
#         background-color: rgba(67, 97, 238, 0.1);
#     }
#     /* Input fields styling */
#     .stTextInput > div > div > input {
#         border-radius: 8px;
#         border: 1px solid #ccc;
#         padding: 10px 15px;
#     }
#     .stTextArea > div > div > textarea {
#         border-radius: 8px;
#         border: 1px solid #ccc;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Function that adds icons to section headers
# def section_header(title, icon):
#     return f"<div class='section-header'>{icon} {title}</div>"

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     text = ""
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         temp_file.write(pdf_file.read())
#         temp_file_path = temp_file.name
    
#     with open(temp_file_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         for page_num in range(len(pdf_reader.pages)):
#             text += pdf_reader.pages[page_num].extract_text()
    
#     os.unlink(temp_file_path)
#     return text

# # Configure Gemini AI
# def configure_gemini(api_key):
#     try:
#         genai.configure(api_key=api_key)
#         return True
#     except Exception as e:
#         st.error(f"Error configuring Gemini AI: {e}")
#         return False

# # Function to analyze resume
# def analyze_resume(resume_text, job_title, job_description):
#     model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
#     prompt = f"""
#     Act as an expert resume analyst and career coach. You are analyzing a resume for a {job_title} position.
    
#     JOB DESCRIPTION:
#     {job_description}
    
#     RESUME:
#     {resume_text}
    
#     Provide a comprehensive analysis of the resume compared to the job requirements. Structure your analysis as follows:
    
#     1. Match Score: Provide a percentage match score between the resume and job description.
    
#     2. Key Strengths: List 3-5 strengths in the resume that align well with the job requirements.
    
#     3. Improvement Areas: List 3-5 specific areas where the resume could be improved to better match the job.
    
#     4. Missing Skills/Keywords: Identify specific skills or keywords from the job description that are missing in the resume.
    
#     5. Format and Presentation: Analyze the structure, organization, and presentation of the resume.
    
#     6. Action Items: Provide 3-5 specific, actionable recommendations to improve the resume for this specific job application.
    
#     Your analysis should be detailed, specific, and actionable. Use bullet points where appropriate for clarity.
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error analyzing resume: {e}"

# # Function to ask questions about the resume
# def ask_question_about_resume(resume_text, job_title, job_description, question):
#     model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
#     prompt = f"""
#     Act as an expert resume analyst and career coach. You are analyzing a resume for a {job_title} position.
    
#     JOB DESCRIPTION:
#     {job_description}
    
#     RESUME:
#     {resume_text}
    
#     QUESTION: {question}
    
#     Provide a detailed, insightful, and helpful response to the question based on your analysis of how the resume matches with the job requirements.
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

# # Function to generate a sample optimized resume
# def generate_sample_resume(resume_text, job_title, job_description, analysis_result):
#     model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    
#     prompt = f"""
#     Act as an expert resume writer. Based on the following information, create a sample optimized resume that would be highly suitable for the {job_title} position.
    
#     ORIGINAL RESUME:
#     {resume_text}
    
#     JOB DESCRIPTION:
#     {job_description}
    
#     ANALYSIS OF THE ORIGINAL RESUME:
#     {analysis_result}
    
#     Create a well-formatted, professional resume that:
#     1. Incorporates the missing skills and keywords identified in the analysis
#     2. Addresses the improvement areas mentioned
#     3. Builds upon the strengths already present in the original resume
#     4. Uses a professional and ATS-friendly format
#     5. Includes all relevant sections (Summary, Experience, Skills, Education, etc.)
    
#     Format the resume in markdown with clear sections and bullet points for readability.
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error generating sample resume: {e}"

# # Function to handle chat messages
# def handle_chat_message(message, resume_text, job_title, job_description, analysis_result):
#     # Check if it's a resume generation request
#     if any(phrase in message.lower() for phrase in ["provide resume", "generate resume", "create resume", "sample resume", "optimized resume"]):
#         st.info("Generating an optimized sample resume based on the analysis...")
#         sample_resume = generate_sample_resume(resume_text, job_title, job_description, analysis_result)
#         return "Here's a sample optimized resume based on our analysis. Use this as a template to improve your own resume:\n\n" + sample_resume
    
#     # Regular chat response
#     model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
#     prompt = f"""
#     You are a helpful resume coach assistant. The user has received an analysis of their resume for a {job_title} position.
    
#     RESUME CONTENT:
#     {resume_text}
    
#     JOB DESCRIPTION:
#     {job_description}
    
#     ANALYSIS RESULTS:
#     {analysis_result}
    
#     USER QUESTION: {message}
    
#     Provide a helpful, supportive, and actionable response to help them improve their resume based on the analysis.
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

# # Function to submit a message to the chat
# def submit_message():
#     user_message = st.session_state.user_input
#     if user_message:
#         # Add user message to chat history
#         st.session_state.chat_history.append({"text": user_message, "is_user": True})
        
#         # Get response
#         with st.spinner("Thinking..."):
#             response_text = handle_chat_message(
#                 user_message,
#                 st.session_state.resume_text,
#                 st.session_state.job_title,
#                 st.session_state.job_description,
#                 st.session_state.analysis_result
#             )
            
#         # Add assistant response to chat history
#         st.session_state.chat_history.append({"text": response_text, "is_user": False})
        
#         # Clear the input by setting our custom session state variable (not the widget state)
#         st.session_state.user_input = ""

# # Main application
# def main():
#     st.markdown("<h1 style='text-align: center;'>🚀 AI Resume Analyzer</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Optimize your resume for your dream job with AI-powered analysis and feedback</p>", unsafe_allow_html=True)
    
#     # Sidebar for API key
#     with st.sidebar:
#         st.header("Configuration")
#         api_key = st.text_input("Enter your Google Gemini API Key", type="password")
#         if api_key:
#             if configure_gemini(api_key):
#                 st.success("Gemini API configured successfully!")
#             else:
#                 st.error("Failed to configure Gemini API. Check your API key.")
        
#         st.markdown("### About")
#         st.info(
#             """
#             This app uses Google's Gemini AI to analyze your resume against job descriptions.
#             Get insights on how well your resume matches the job requirements and receive
#             personalized recommendations to improve your chances.
#             """
#         )

#     # Tabs for different functionalities
#     tab1, tab2 = st.tabs(["Resume Analysis", "Ask Questions"])
    
#     # Resume Analysis Tab
#     with tab1:
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown(section_header("📄 Upload Your Resume", "📤"), unsafe_allow_html=True)
#             with st.container():
#                 st.markdown('<div class="upload-section">', unsafe_allow_html=True)
#                 uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
                
#                 if uploaded_file is not None:
#                     st.success("✅ Resume uploaded successfully!")
#                     try:
#                         resume_text = extract_text_from_pdf(uploaded_file)
#                         st.session_state.resume_text = resume_text  # Store in session state
#                         with st.expander("🔍 Preview Extracted Text"):
#                             st.text(resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
#                     except Exception as e:
#                         st.error(f"Error extracting text from PDF: {e}")
#                         resume_text = ""
#                         st.session_state.resume_text = ""
#                 else:
#                     st.info("📁 Please upload your resume in PDF format")
#                     resume_text = ""
#                     if 'resume_text' not in st.session_state:
#                         st.session_state.resume_text = ""
#                 st.markdown('</div>', unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(section_header("💼 Job Details", "📋"), unsafe_allow_html=True)
#             with st.container():
#                 st.markdown('<div class="job-details-section">', unsafe_allow_html=True)
#                 job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist")
#                 st.session_state.job_title = job_title
                
#                 job_description = st.text_area("Job Description", height=200, 
#                                     placeholder="Paste the job description here...")
#                 st.session_state.job_description = job_description
#                 st.markdown('</div>', unsafe_allow_html=True)
        
#         # Analyze button with enhanced styling
#         col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
#         with col_btn2:
#             analyze_button = st.button(
#                 "🔍 Analyze Resume", 
#                 key="analyze_btn", 
#                 disabled=not (api_key and resume_text and job_title and job_description)
#             )
        
#         # Analysis section - always show if there's an analysis result
#         if st.session_state.analysis_result:
#             st.markdown(section_header("📊 Analysis Results", "🎯"), unsafe_allow_html=True)
#             st.markdown('<div class="result-container">', unsafe_allow_html=True)
#             st.markdown(st.session_state.analysis_result)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Process the analysis when button is clicked
#         if analyze_button:
#             with st.spinner("⏳ Analyzing your resume..."):
#                 analysis = analyze_resume(resume_text, job_title, job_description)
#                 st.session_state.analysis_result = analysis
                
#                 # Show the analysis after it's done
#                 st.markdown(section_header("📊 Analysis Results", "🎯"), unsafe_allow_html=True)
#                 st.markdown('<div class="result-container">', unsafe_allow_html=True)
#                 st.markdown(analysis)
#                 st.markdown('</div>', unsafe_allow_html=True)
                
#         # Chat section - always show if there's an analysis result
#         if st.session_state.analysis_result:
#             st.markdown(section_header("💬 Ask Follow-up Questions", "❓"), unsafe_allow_html=True)
#             st.write("Ask questions about the analysis or request specific feedback about your resume")
            
#             # Create a container for chat messages with better styling
#             chat_container = st.container()
            
#             # Display chat history in the container with improved styling
#             with chat_container:
#                 for message in st.session_state.chat_history:
#                     if message["is_user"]:
#                         st.markdown(f'<div class="chat-user"><strong>You:</strong> {message["text"]}</div>', unsafe_allow_html=True)
#                     else:
#                         st.markdown(f'<div class="chat-ai"><strong>AI Assistant:</strong> {message["text"]}</div>', unsafe_allow_html=True)
            
#             # Chat input with a send button - better styled
#             col1, col2 = st.columns([5, 1])  # Adjust the ratio as needed
            
#             with col1:
#                 # Text input without on_change callback
#                 st.text_input(
#                     "Type your question here:", 
#                     key="chat_input",
#                     placeholder="e.g., How can I improve my technical skills section?",
#                     value=st.session_state.user_input,
#                     # No on_change parameter here
#                 )
                
#                 # Update user_input whenever chat_input changes
#                 st.session_state.user_input = st.session_state.chat_input
            
#             with col2:
#                 # Add some vertical space to align the button with the input field
#                 st.write("")
#                 # Add the send button
#                 if st.button("Send ✉️", key="send_button"):
#                     submit_message()
#                     # Use st.rerun() instead of st.experimental_rerun()
#                     st.rerun()
    
#     # Ask Questions Tab - With improved styling
#     with tab2:
#         if not st.session_state.resume_text:
#             st.info("📋 Please upload your resume in the 'Resume Analysis' tab first.")
#         elif not st.session_state.job_title or not st.session_state.job_description:
#             st.info("💼 Please enter job details in the 'Resume Analysis' tab first.")
#         else:
#             st.markdown(section_header("❓ Ask Questions About Your Resume", "🔍"), unsafe_allow_html=True)
#             st.write("Ask anything about how your resume fits the job or how to improve it.")
            
#             with st.container():
#                 st.markdown('<div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
#                 question = st.text_area("Your Question", placeholder="e.g., What are the top 3 skills I should add to my resume for this job?")
                
#                 col_q1, col_q2, col_q3 = st.columns([1, 2, 1])
#                 with col_q2:
#                     ask_button = st.button("Get Answer 🔍", key="question_btn", disabled=not (api_key and question))
#                 st.markdown('</div>', unsafe_allow_html=True)
                
#                 if ask_button:
#                     with st.spinner("⏳ Thinking..."):
#                         answer = ask_question_about_resume(st.session_state.resume_text, st.session_state.job_title, st.session_state.job_description, question)
                    
#                     st.markdown(section_header("💬 Answer", "✨"), unsafe_allow_html=True)
#                     st.markdown('<div class="result-container">', unsafe_allow_html=True)
#                     st.markdown(answer)
#                     st.markdown('</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

import streamlit as st
import os
import tempfile
import PyPDF2
import google.generativeai as genai
import time
from typing import Optional

# Set page configuration
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "gemini-2.0-flash"

# Custom CSS - WHITE BACKGROUND REMOVED FROM ANALYSIS CONTAINER
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    /* ANALYSIS CONTAINER - WHITE BACKGROUND REMOVED */
    .analysis-container {
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
    }
    .upload-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 2px dashed #667eea;
    }
    .match-score {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    .section-title {
        color: #2d3748;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .chat-user {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px 12px 12px 4px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-ai {
        background: #f7fafc;
        color: #2d3748;
        padding: 1rem;
        border-radius: 12px 12px 4px 12px;
        margin: 0.5rem 0;
        max-width: 80%;
        border: 1px solid #e2e8f0;
    }
    .success-box {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fffaf0;
        border: 1px solid #fbd38d;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #fff5f5;
        border: 1px solid #fc8181;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #ebf8ff;
        border: 1px solid #90cdf4;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    /* Additional styles for transparent background */
    .transparent-bg {
        background: transparent !important;
    }
    .analysis-content {
        padding: 1rem;
        line-height: 1.6;
    }
    .analysis-content h3 {
        color: #2d3748;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .analysis-content ul, .analysis-content ol {
        padding-left: 1.5rem;
        margin: 0.5rem 0;
    }
    .analysis-content li {
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Function to configure Gemini
def configure_gemini(api_key: str) -> bool:
    """Configure Gemini AI with API key"""
    try:
        genai.configure(api_key=api_key)
        st.session_state.api_key = api_key
        return True
    except Exception as e:
        st.error(f"Error configuring Gemini: {e}")
        return False

# Function to get Gemini model
def get_gemini_model(model_name: str = None) -> Optional[genai.GenerativeModel]:
    """Get Gemini model instance"""
    try:
        if not st.session_state.api_key:
            return None
        
        genai.configure(api_key=st.session_state.api_key)
        
        # Use selected model or default
        if not model_name:
            model_name = st.session_state.selected_model
        
        # Try to get the model
        try:
            model = genai.GenerativeModel(model_name)
            # Test with a small prompt
            test_response = model.generate_content("Test")
            if test_response and test_response.text:
                return model
        except Exception as e:
            st.warning(f"Model {model_name} failed: {str(e)[:100]}")
            
            # Fallback models in order of preference
            fallback_models = [
                'gemini-2.0-flash',
                'gemini-2.0-flash-001',
                'gemini-pro-latest',
                'gemini-2.0-flash-lite',
                'gemini-1.5-flash-latest'
            ]
            
            for fallback in fallback_models:
                try:
                    model = genai.GenerativeModel(fallback)
                    test_response = model.generate_content("Test")
                    if test_response.text:
                        st.session_state.selected_model = fallback
                        st.info(f"Using fallback model: {fallback}")
                        return model
                except:
                    continue
            
            return None
            
    except Exception as e:
        st.error(f"Error getting model: {e}")
        return None

# Basic analysis without API
def analyze_resume_basic(resume_text: str, job_title: str, job_description: str) -> str:
    """Perform basic keyword analysis without API"""
    
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Common skills to check
    skills_list = [
        'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'angular',
        'node.js', 'aws', 'azure', 'docker', 'kubernetes', 'machine learning',
        'data analysis', 'excel', 'power bi', 'tableau', 'project management',
        'agile', 'scrum', 'leadership', 'communication', 'teamwork', 'problem solving',
        'analytical skills', 'time management', 'creativity', 'adaptability'
    ]
    
    # Find skills in job description
    job_skills = []
    for skill in skills_list:
        if skill in job_lower:
            job_skills.append(skill)
    
    # Find matching skills in resume
    matching_skills = []
    for skill in job_skills:
        if skill in resume_lower:
            matching_skills.append(skill)
    
    # Calculate match score
    if job_skills:
        match_score = int((len(matching_skills) / len(job_skills)) * 100)
    else:
        match_score = 50
    
    # Prepare analysis - WITHOUT WHITE BACKGROUND
    analysis = f"""
<div class="analysis-container transparent-bg">
    <div class="match-score">Match Score: {match_score}%</div>
    
    <div class="section-title">📊 Analysis Summary</div>
    
    <div class="analysis-content">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin: 1.5rem 0;">
            <div>
                <h4>✅ Found Skills ({len(matching_skills)})</h4>
                <ul>
                    {''.join([f'<li>{skill.title()}</li>' for skill in matching_skills[:10]])}
                </ul>
            </div>
            
            <div>
                <h4>❌ Missing Skills ({len(job_skills) - len(matching_skills)})</h4>
                <ul>
                    {''.join([f'<li>{skill.title()}</li>' for skill in list(set(job_skills) - set(matching_skills))[:10]])}
                </ul>
            </div>
        </div>
        
        <div class="section-title">💡 Recommendations</div>
        
        <div style="background: rgba(248, 250, 252, 0.5); padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <ol>
                <li><strong>Add Missing Keywords:</strong> Incorporate {', '.join(list(set(job_skills) - set(matching_skills))[:3]) if len(job_skills) > len(matching_skills) else 'relevant keywords'} naturally into your resume.</li>
                <li><strong>Quantify Achievements:</strong> Use numbers and metrics (e.g., "Increased efficiency by 30%", "Managed team of 10").</li>
                <li><strong>Use Action Verbs:</strong> Start bullet points with strong verbs like: Achieved, Built, Created, Developed, Improved, Led, Managed, Optimized.</li>
                <li><strong>Tailor Your Resume:</strong> Customize your resume specifically for this {job_title} position.</li>
                <li><strong>Check Format:</strong> Ensure your resume is clean, professional, and 1-2 pages maximum.</li>
            </ol>
        </div>
    </div>
    
    <div class="warning-box">
        <strong>Note:</strong> This is a basic keyword analysis. For comprehensive AI-powered analysis with detailed insights, 
        add your Gemini API key in the sidebar.
    </div>
</div>
"""
    return analysis

# AI-powered analysis
def analyze_resume_ai(resume_text: str, job_title: str, job_description: str) -> str:
    """Perform AI-powered resume analysis using Gemini"""
    
    model = get_gemini_model()
    if model is None:
        return "⚠️ Could not connect to AI service. Please check your API key."
    
    # Prepare prompt
    prompt = f"""You are an expert resume analyst and career coach. Analyze this resume for a {job_title} position.

JOB DESCRIPTION:
{job_description[:2000]}

RESUME CONTENT:
{resume_text[:3000]}

Please provide a comprehensive analysis including:

1. **Overall Match Score** (as a percentage 0-100%)
2. **Key Strengths** (3-5 points that align well with the job)
3. **Areas for Improvement** (3-5 specific areas to work on)
4. **Missing Keywords/Skills** (from job description that are missing in resume)
5. **Actionable Recommendations** (3-5 specific, actionable steps to improve)

Format your response professionally with clear sections. Start with the match score prominently displayed.

IMPORTANT: Make sure to include "Match Score: XX%" at the beginning where XX is the percentage."""

    try:
        with st.spinner("🤖 AI is analyzing your resume..."):
            response = model.generate_content(prompt)
            
        if response and response.text:
            # Ensure match score is properly formatted
            result = response.text
            if "Match Score:" not in result:
                result = f"Match Score: (Analyzed by AI)\n\n{result}"
            
            return result
        else:
            return "❌ No response received from AI. Please try again."
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return "⚠️ API rate limit exceeded. Please wait a minute and try again, or use the basic analysis."
        elif "503" in error_msg or "unavailable" in error_msg.lower():
            return "🔧 Service temporarily unavailable. Please try again shortly."
        else:
            return f"❌ Error: {error_msg[:150]}"

# Function to handle chat questions
def ask_resume_question(question: str, context: str) -> str:
    """Handle chat questions about resume"""
    model = get_gemini_model()
    if model is None:
        return "Please configure your API key first."
    
    prompt = f"""You are a helpful career coach. Answer this question based on the resume analysis:

CONTEXT:
{context[:1500]}

QUESTION: {question}

Provide a helpful, specific, and actionable answer. Keep it concise and practical."""

    try:
        response = model.generate_content(prompt)
        return response.text if response and response.text else "No response received."
    except Exception as e:
        return f"Error: {str(e)[:100]}"

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 AI Resume Analyzer Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your resume and get AI-powered insights to land your dream job</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key Input
        api_key = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            help="Get your free API key from https://makersuite.google.com/app/apikey",
            value=st.session_state.get('api_key', '')
        )
        
        if api_key and api_key != st.session_state.get('api_key', ''):
            if configure_gemini(api_key):
                st.markdown('<div class="success-box">✅ API Key Configured Successfully!</div>', unsafe_allow_html=True)
        
        # Model Selection
        st.markdown("### 🤖 AI Model")
        model_options = [
            "gemini-2.0-flash (Fast & Efficient)",
            "gemini-2.0-flash-001",
            "gemini-pro-latest",
            "gemini-2.0-flash-lite",
            "gemini-2.5-flash"
        ]
        
        selected_model_display = st.selectbox(
            "Select Model",
            model_options,
            index=0
        )
        
        # Extract model name from display
        if "gemini-2.0-flash (Fast & Efficient)" in selected_model_display:
            st.session_state.selected_model = "gemini-2.0-flash"
        else:
            st.session_state.selected_model = selected_model_display.split()[0]
        
        st.markdown("---")
        
        # Quick Tips
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        1. **Upload PDF** resumes only
        2. **Copy-paste** full job description
        3. **Use API key** for best results
        4. **Review** all recommendations
        5. **Customize** resume for each job
        """)
        
        # About
        with st.expander("ℹ️ About This Tool"):
            st.markdown("""
            This AI Resume Analyzer helps you:
            - 📊 Get match score with job
            - ✅ Identify strengths
            - ⚠️ Find improvement areas
            - 💡 Get actionable advice
            - 💬 Ask follow-up questions
            """)
    
    # Main content in tabs
    tab1, tab2 = st.tabs(["📄 Resume Analysis", "💬 Ask Questions"])
    
    with tab1:
        # Two column layout for upload and job details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 Upload Your Resume")
            st.markdown('<div class="upload-box">', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Drag and drop or click to upload PDF",
                type=['pdf'],
                label_visibility="collapsed",
                key="resume_uploader"
            )
            
            if uploaded_file is not None:
                # Extract text from PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    st.session_state.resume_text = resume_text
                    
                    # Show resume info
                    file_size = len(uploaded_file.getvalue()) / 1024  # KB
                    word_count = len(resume_text.split())
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("📏 File Size", f"{file_size:.1f} KB")
                    with col_b:
                        st.metric("📝 Word Count", f"{word_count}")
                    
                    # Preview
                    with st.expander("👁️ Preview Resume Text", expanded=False):
                        st.text_area(
                            "",
                            value=resume_text[:800] + "..." if len(resume_text) > 800 else resume_text,
                            height=200,
                            disabled=True
                        )
                else:
                    st.error("Could not extract text from PDF. Please try another file.")
            else:
                st.info("📁 Upload your resume in PDF format")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💼 Job Details")
            st.markdown('<div class="upload-box">', unsafe_allow_html=True)
            
            job_title = st.text_input(
                "Job Title*",
                placeholder="e.g., Data Scientist, Software Engineer, Marketing Manager",
                value=st.session_state.get('job_title', '')
            )
            st.session_state.job_title = job_title
            
            job_description = st.text_area(
                "Job Description*",
                height=250,
                placeholder="Paste the complete job description here...",
                value=st.session_state.get('job_description', '')
            )
            st.session_state.job_description = job_description
            
            if job_description:
                word_count = len(job_description.split())
                st.caption(f"📊 Job description: {word_count} words")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Analyze Button
        st.markdown("---")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_disabled = not (st.session_state.resume_text and 
                                   st.session_state.job_title and 
                                   st.session_state.job_description)
            
            analyze_clicked = st.button(
                "🔍 ANALYZE RESUME NOW",
                type="primary",
                disabled=analyze_disabled,
                use_container_width=True
            )
        
        # Perform Analysis
        if analyze_clicked:
            with st.spinner("Analyzing your resume..."):
                if st.session_state.api_key:
                    # Use AI analysis
                    result = analyze_resume_ai(
                        st.session_state.resume_text,
                        st.session_state.job_title,
                        st.session_state.job_description
                    )
                else:
                    # Use basic analysis
                    result = analyze_resume_basic(
                        st.session_state.resume_text,
                        st.session_state.job_title,
                        st.session_state.job_description
                    )
                
                st.session_state.analysis_result = result
        
        # Display Results - WITHOUT EXTRA CONTAINER
        if st.session_state.analysis_result:
            st.markdown("---")
            st.markdown("### 📋 Analysis Results")
            
            # Check if result is HTML or plain text
            if "<div" in st.session_state.analysis_result:
                st.markdown(st.session_state.analysis_result, unsafe_allow_html=True)
            else:
                # For plain text results, format with transparent background
                st.markdown(f"""
                <div class="analysis-container transparent-bg">
                    <div class="analysis-content">
                        {st.session_state.analysis_result}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 💬 Chat with Resume Coach")
        
        if not st.session_state.analysis_result:
            st.info("👈 First analyze your resume in the 'Resume Analysis' tab")
        else:
            # Display chat history
            chat_container = st.container()
            
            with chat_container:
                for i, message in enumerate(st.session_state.chat_history[-10:]):  # Last 10 messages
                    if message["is_user"]:
                        st.markdown(f'<div class="chat-user">{message["text"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-ai">{message["text"]}</div>', unsafe_allow_html=True)
            
            # Chat input
            st.markdown("---")
            
            col_input1, col_input2 = st.columns([5, 1])
            
            with col_input1:
                user_question = st.text_input(
                    "Ask a question about your resume analysis:",
                    placeholder="e.g., How can I improve my technical skills section?",
                    label_visibility="collapsed",
                    key="chat_input"
                )
            
            with col_input2:
                st.write("")  # Spacing
                ask_button = st.button("Send", use_container_width=True)
            
            if ask_button and user_question:
                if not st.session_state.api_key:
                    st.warning("Please add your API key in the sidebar to use chat features.")
                else:
                    # Add user message to history
                    st.session_state.chat_history.append({
                        "text": user_question,
                        "is_user": True
                    })
                    
                    # Get AI response
                    with st.spinner("Thinking..."):
                        ai_response = ask_resume_question(
                            user_question,
                            st.session_state.analysis_result
                        )
                    
                    # Add AI response to history
                    st.session_state.chat_history.append({
                        "text": ai_response,
                        "is_user": False
                    })
                    
                    # Rerun to show new messages
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem;">
    <p>Made with ❤️ using Streamlit & Google Gemini AI | Upload PDF resumes only</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()