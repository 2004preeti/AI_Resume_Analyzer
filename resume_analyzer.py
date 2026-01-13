
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
import requests
import json
import re
from datetime import datetime

# ===============================
# Streamlit Configuration
# ===============================
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Session State Variables
# ===============================
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_title' not in st.session_state:
    st.session_state.job_title = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'api_mode' not in st.session_state:
    st.session_state.api_mode = "offline"

# ===============================
# Custom CSS - Updated Colors
# ===============================
st.markdown("""
<style>
    .main {padding: 20px;}
    .stButton>button {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px;}
    .result-box {border-left: 5px solid #667eea; padding: 25px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); margin: 20px 0; border-radius: 10px;}
    
    /* Token box with gradient purple background */
    .token-box {background: linear-gradient(135deg, #9c27b0 0%, #673ab7 100%); padding: 20px; border-radius: 10px; margin: 15px 0; border: 2px solid #7b1fa2; color: white; font-weight: bold;}
    .token-box a {color: #ffeb3b !important; font-weight: bold; text-decoration: underline;}
    .token-box a:hover {color: #fff176 !important;}
    
    /* Tip box - Light blue */
    .tip-box {background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid #bbdefb;}
    
    /* API status boxes */
    .api-success {background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); color: white; padding: 15px; border-radius: 10px; border: 1px solid #388E3C;}
    .api-warning {background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); color: white; padding: 15px; border-radius: 10px; border: 1px solid #FFA726;}
    .api-error {background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); color: white; padding: 15px; border-radius: 10px; border: 1px solid #e53935;}
    
    /* Header with gradient */
    .header-text {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center;}
    
    /* Metric boxes */
    .metric-box {background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;}
    
    /* Mode selection cards */
    .mode-card {padding: 15px; border-radius: 10px; margin: 10px 0; transition: transform 0.3s ease;}
    .mode-card:hover {transform: translateY(-5px);}
    .mode-offline {background: linear-gradient(135deg, #78909c 0%, #546e7a 100%); color: white;}
    .mode-huggingface {background: linear-gradient(135deg, #ff6f00 0%, #e65100 100%); color: white;}
    .mode-openrouter {background: linear-gradient(135deg, #00acc1 0%, #00838f 100%); color: white;}
    .mode-deepseek {background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); color: white;}
    
    /* Input fields */
    .stTextInput>div>div>input {border-radius: 8px !important; border: 2px solid #667eea !important;}
    .stTextArea>div>div>textarea {border-radius: 8px !important; border: 2px solid #667eea !important;}
    
    /* Sidebar styling */
    .css-1d391kg {background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);}
    
    /* Selection highlight */
    .selected-mode {border: 3px solid #ffeb3b !important; box-shadow: 0 0 15px rgba(255, 235, 59, 0.5);}
    
    /* Preview text styling */
    .preview-text {font-family: monospace; font-size: 12px; line-height: 1.5; white-space: pre-wrap;}
</style>
""", unsafe_allow_html=True)

# ===============================
# API Configuration
# ===============================
class APIManager:
    def __init__(self):
        self.services = {
            "huggingface": {
                "name": "🤗 Hugging Face",
                "icon": "🤗",
                "url": "https://api-inference.huggingface.co/models/{model}",
                "models": ["mistralai/Mistral-7B-Instruct-v0.1", "google/flan-t5-xxl", "gpt2"],
                "requires_token": True,
                "color": "#ff6f00"
            },
            "openrouter": {
                "name": "🔄 OpenRouter",
                "icon": "🔄",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "models": ["mistralai/mistral-7b-instruct", "google/gemma-7b-it"],
                "requires_token": False,
                "free_key": "free",
                "color": "#ff6f00"
            },
            "deepseek": {
                "name": "🔍 DeepSeek",
                "icon": "🔍",
                "url": "https://api.deepseek.com/v1/chat/completions",
                "models": ["deepseek-chat"],
                "requires_token": False,
                "free_key": "sk-free",
                "color": "#ff6f00"
            },
            "offline": {
                "name": "📴 Offline",
                "icon": "📴",
                "models": ["Local Analyzer"],
                "requires_token": False,
                "color": "#ff6f00"
            }
        }
    
    def test_api_connection(self, service_name, api_key=""):
        """Test if API service is available"""
        service = self.services.get(service_name)
        if not service:
            return False, "Service not found"
        
        if service_name == "offline":
            return True, "Offline mode always available"
        
        try:
            if service_name == "huggingface":
                url = service["url"].format(model="gpt2")
                headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
                response = requests.get(url, headers=headers, timeout=10)
                return response.status_code == 200, f"Status: {response.status_code}"
            
            elif service_name == "openrouter":
                headers = {
                    "Authorization": f"Bearer {service['free_key']}",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "Resume Analyzer"
                }
                response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
                return response.status_code == 200, f"Status: {response.status_code}"
            
            elif service_name == "deepseek":
                headers = {"Authorization": f"Bearer {service['free_key']}"}
                response = requests.get("https://api.deepseek.com/v1/models", headers=headers, timeout=10)
                return response.status_code == 200, f"Status: {response.status_code}"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
        
        return False, "Unknown error"

# ===============================
# PDF Processing
# ===============================
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"PDF extraction error: {str(e)}")
        return ""

# ===============================
# Offline Analysis Engine
# ===============================
class OfflineAnalyzer:
    def __init__(self):
        self.common_keywords = {
            'technical': ['python', 'java', 'javascript', 'sql', 'aws', 'azure', 'docker', 'kubernetes', 
                         'machine learning', 'data analysis', 'web development', 'api', 'react', 'node.js'],
            'soft': ['leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
                    'project management', 'time management', 'adaptability', 'creativity'],
            'business': ['strategy', 'budget', 'revenue', 'growth', 'efficiency', 'optimization',
                        'stakeholder', 'analysis', 'reporting', 'presentation']
        }
    
    def analyze(self, resume_text, job_title, job_description):
        """Perform offline analysis"""
        # Extract keywords
        job_keywords = self._extract_keywords(job_description)
        resume_keywords = self._extract_keywords(resume_text)
        
        # Calculate metrics
        match_score = self._calculate_match_score(job_keywords, resume_keywords)
        strengths = self._identify_strengths(resume_text, job_keywords)
        improvements = self._identify_improvements(resume_text, job_keywords)
        missing_keywords = self._find_missing_keywords(job_keywords, resume_keywords)
        
        # Generate report
        report = self._generate_report(match_score, strengths, improvements, missing_keywords, 
                                      job_title, len(resume_text))
        return report
    
    def _extract_keywords(self, text):
        """Extract keywords from text"""
        if not text:
            return []
        
        # Convert to lowercase and find words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {'with', 'this', 'that', 'have', 'from', 'which', 'their', 'would', 'should'}
        keywords = [word for word in words if word not in stop_words]
        
        # Add specific skills if mentioned
        all_skills = []
        for category in self.common_keywords.values():
            all_skills.extend(category)
        
        found_skills = [skill for skill in all_skills if skill in text.lower()]
        
        return list(set(keywords[:30] + found_skills))
    
    def _calculate_match_score(self, job_keywords, resume_keywords):
        """Calculate match percentage"""
        if not job_keywords:
            return 65
        
        matched = set(job_keywords) & set(resume_keywords)
        score = int((len(matched) / len(job_keywords)) * 100)
        return min(max(score, 30), 95)
    
    def _identify_strengths(self, resume_text, job_keywords):
        """Identify strengths in resume"""
        strengths = []
        
        # Check structure
        sections = ['experience', 'education', 'skills', 'projects', 'summary']
        found_sections = [section for section in sections if section in resume_text.lower()]
        
        if len(found_sections) >= 3:
            strengths.append(f"Good structure with {len(found_sections)} key sections")
        
        # Check length
        word_count = len(resume_text.split())
        if 300 <= word_count <= 800:
            strengths.append(f"Optimal length ({word_count} words)")
        
        # Check contact info
        contact_patterns = [r'\b[\w\.-]+@[\w\.-]+\.\w{2,}\b', r'\+\d{10,}', r'linkedin\.com']
        contact_found = any(re.search(pattern, resume_text, re.IGNORECASE) for pattern in contact_patterns)
        if contact_found:
            strengths.append("Contact information included")
        
        return strengths if strengths else ["Resume format is clean and readable"]
    
    def _identify_improvements(self, resume_text, job_keywords):
        """Identify areas for improvement"""
        improvements = []
        
        # Check for numbers/quantification
        numbers = re.findall(r'\b\d+%\b|\b\d+\s*\%\b|\$\d+|\d+\s*(years|months)', resume_text)
        if len(numbers) < 2:
            improvements.append("Add more quantifiable achievements (use numbers)")
        
        # Check action verbs
        action_verbs = ['managed', 'developed', 'created', 'increased', 'reduced', 'improved', 
                       'led', 'implemented', 'designed', 'optimized']
        verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
        if verb_count < 3:
            improvements.append("Use more action verbs to start bullet points")
        
        # Check keywords match
        if job_keywords:
            matched_keywords = [kw for kw in job_keywords if kw in resume_text.lower()]
            if len(matched_keywords) < len(job_keywords) * 0.3:
                improvements.append("Increase keyword matching with job description")
        
        return improvements if improvements else ["Review for consistency and formatting"]
    
    def _find_missing_keywords(self, job_keywords, resume_keywords):
        """Find keywords from JD missing in resume"""
        if not job_keywords:
            return ["technical skills", "relevant experience", "achievements"]
        
        missing = set(job_keywords[:10]) - set(resume_keywords)
        return list(missing)[:5] if missing else ["industry-specific terms"]
    
    def _generate_report(self, score, strengths, improvements, missing_keywords, job_title, resume_length):
        """Generate formatted analysis report"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        report = f"""
        🚀 **AI RESUME ANALYSIS REPORT**
        ================================
        **Job Target:** {job_title if job_title else "Not specified"}
        **Analysis Date:** {current_date}
        **Resume Length:** {resume_length} characters
        
        📊 **MATCH SCORE:** **{score}/100**
        
        ✅ **KEY STRENGTHS:**
        {chr(10).join(['• ' + s for s in strengths])}
        
        ⚠️ **AREAS FOR IMPROVEMENT:**
        {chr(10).join(['• ' + i for i in improvements])}
        
        🔍 **MISSING KEYWORDS:**
        {chr(10).join(['• ' + mk.title() for mk in missing_keywords])}
        
        💡 **ACTIONABLE RECOMMENDATIONS:**
        • Quantify achievements with specific numbers
        • Start each bullet point with strong action verbs
        • Tailor resume specifically for each job application
        • Include relevant certifications and projects
        • Proofread for spelling and grammar errors
        
        🎯 **NEXT STEPS:**
        1. Review job description and add missing keywords
        2. Add 3-5 quantifiable achievements
        3. Optimize for ATS (Applicant Tracking System)
        4. Get feedback from peers or mentors
        5. Save final version as PDF
        
        *Generated using Smart Resume Analyzer | Offline Mode*
        """
        return report

# ===============================
# Online API Analysis
# ===============================
class OnlineAnalyzer:
    def __init__(self, api_manager):
        self.api_manager = api_manager
    
    def analyze_with_api(self, prompt, service_name="huggingface", api_key="", model=""):
        """Analyze using online API"""
        service = self.api_manager.services.get(service_name)
        if not service:
            return "Service not available"
        
        try:
            if service_name == "huggingface":
                return self._call_huggingface(prompt, model, api_key)
            elif service_name == "openrouter":
                return self._call_openrouter(prompt, model)
            elif service_name == "deepseek":
                return self._call_deepseek(prompt, model)
        except Exception as e:
            return f"API Error: {str(e)}"
        
        return "API service unavailable"
    
    def _call_huggingface(self, prompt, model, api_key):
        """Call Hugging Face API"""
        if not model:
            model = "gpt2"
        
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
        payload = {
            "inputs": prompt[:1500],
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", str(data))
            return str(data)
        else:
            return f"Hugging Face Error: {response.status_code}"
    
    def _call_openrouter(self, prompt, model):
        """Call OpenRouter API (free tier)"""
        if not model:
            model = "mistralai/mistral-7b-instruct"
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": "Bearer free",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Resume Analyzer",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"OpenRouter Error: {response.status_code}"
    
    def _call_deepseek(self, prompt, model):
        """Call DeepSeek API (free tier)"""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": "Bearer sk-free",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"DeepSeek Error: {response.status_code}"

# ===============================
# Main Application
# ===============================
def main():
    # Initialize managers
    api_manager = APIManager()
    offline_analyzer = OfflineAnalyzer()
    online_analyzer = OnlineAnalyzer(api_manager)
    
    # Header with gradient
    st.markdown("""
    <div class="header-text">
        <h1 style="margin:0;">📝 AI Resume Analyzer Pro</h1>
        <p style="margin:5px 0 0 0; font-size:1.2em;">Smart Analysis with Online & Offline Modes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Mode Selection with Cards
        st.markdown("#### 🔧 Select Analysis Mode")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📴 Offline", use_container_width=True, 
                        help="No API required. Fast and private."):
                st.session_state.api_mode = "offline"
                st.rerun()
        
        with col2:
            if st.button("🤗 Hugging Face", use_container_width=True,
                        help="Requires API token. Most powerful."):
                st.session_state.api_mode = "huggingface"
                st.rerun()
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🔄 OpenRouter", use_container_width=True,
                        help="Free API. No token required."):
                st.session_state.api_mode = "openrouter"
                st.rerun()
        
        with col4:
            if st.button("🔍 DeepSeek", use_container_width=True,
                        help="Free API. No token required."):
                st.session_state.api_mode = "deepseek"
                st.rerun()
        
        # Current mode indicator
        current_mode = st.session_state.api_mode
        mode_info = api_manager.services.get(current_mode, {})
        mode_color = mode_info.get('color', '#78909c')
        mode_name = mode_info.get('name', 'Offline')
        
        st.markdown(f"""
        <div style="background: {mode_color}; color: white; padding: 10px; border-radius: 8px; text-align: center; margin: 10px 0;">
            <strong>Current Mode:</strong> {mode_name}
        </div>
        """, unsafe_allow_html=True)
        
        # API Configuration based on mode
        api_key = ""
        selected_model = ""
        
        if current_mode == "huggingface":
            # Updated Token Box with Purple Gradient Background
            st.markdown("""
            <div class="token-box">
                <strong>🔑 Get Your Free Token:</strong><br>
                <a href="https://huggingface.co/settings/tokens" target="_blank" style="color: #ffeb3b; text-decoration: underline;">
                    👉 Click Here: huggingface.co/settings/tokens
                </a><br><br>
                <small>1. Sign up / Log in to Hugging Face<br>
                2. Go to Settings → Tokens<br>
                3. Click "New token"<br>
                4. Select "Read" access<br>
                5. Copy and paste below</small>
            </div>
            """, unsafe_allow_html=True)
            
            api_key = st.text_input(
                "Enter Hugging Face Token",
                type="password",
                placeholder="hf_xxxxxxxxxxxxxxxx",
                help="Token should start with 'hf_'"
            )
            
            selected_model = st.selectbox(
                "Select Model",
                api_manager.services["huggingface"]["models"],
                help="Choose AI model for analysis"
            )
            
            # Test Connection Button
            if api_key:
                if st.button("🔗 Test Connection", use_container_width=True):
                    with st.spinner("Testing connection..."):
                        success, message = api_manager.test_api_connection("huggingface", api_key)
                        if success:
                            st.markdown('<div class="api-success">✅ Connection Successful!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="api-error">❌ {message}</div>', unsafe_allow_html=True)
        
        elif current_mode == "openrouter":
            st.markdown("""
            <div class="tip-box">
                <strong>🆓 Free Public API</strong><br>
                No token required! Using OpenRouter's free tier.<br>
                <small>Rate limits may apply. For unlimited use, get API key from <a href="https://openrouter.ai/keys" target="_blank">openrouter.ai</a></small>
            </div>
            """, unsafe_allow_html=True)
            
            selected_model = st.selectbox(
                "Select Model",
                api_manager.services["openrouter"]["models"]
            )
            
            if st.button("🔗 Test Connection", use_container_width=True):
                with st.spinner("Testing connection..."):
                    success, message = api_manager.test_api_connection("openrouter")
                    if success:
                        st.markdown('<div class="api-success">✅ Connection Successful!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="api-warning">⚠️ {message}</div>', unsafe_allow_html=True)
        
        elif current_mode == "deepseek":
            st.markdown("""
            <div class="token-box">
                <strong>🆓 Free Public API</strong><br>
                No token required! Using DeepSeek's free tier.<br>
                <small>Rate limits may apply. For unlimited use, sign up at <a href="https://platform.deepseek.com/api_keys" target="_blank">deepseek.com</a></small>
            </div>
            """, unsafe_allow_html=True)
            
            selected_model = st.selectbox(
                "Select Model",
                api_manager.services["deepseek"]["models"]
            )
            
            if st.button("🔗 Test Connection", use_container_width=True):
                with st.spinner("Testing connection..."):
                    success, message = api_manager.test_api_connection("deepseek")
                    if success:
                        st.markdown('<div class="api-success">✅ Connection Successful!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="api-warning">⚠️ {message}</div>', unsafe_allow_html=True)
        
        else:  # offline
            st.markdown("""
            <div class="token-box">
                <strong>🔒 Privacy Mode</strong><br>
                Your data stays on your device.<br>
                No internet required.<br>
                <small>Basic analysis with keyword matching</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Quick Stats
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            resume_len = len(st.session_state.resume_text) if st.session_state.resume_text else 0
            st.metric("Resume Length", f"{resume_len} chars")
        
        with col2:
            job_display = st.session_state.job_title[:12] + "..." if st.session_state.job_title and len(st.session_state.job_title) > 12 else st.session_state.job_title or "N/A"
            st.metric("Job Title", job_display)
        
        st.divider()
        
        # Tips Section
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        <div class="token-box">
            <strong>For Best Results:</strong><br>
            1. <strong>OpenRouter/DeepSeek:</strong> Best free options<br>
            2. <strong>Hugging Face:</strong> Most powerful (needs token)<br>
            3. <strong>Offline:</strong> Privacy first<br>
            4. Always tailor resume for each job<br>
            5. Quantify achievements with numbers<br>
            6. Use action verbs<br>
            7. Check for spelling errors
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content Area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 Upload Resume")
        
        uploaded_file = st.file_uploader(
            "Choose PDF file", 
            type=['pdf'], 
            key="resume_uploader",
            help="Upload your resume in PDF format"
        )
        
        if uploaded_file:
            with st.spinner("📖 Extracting text from PDF..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.success(f"✅ Resume uploaded! ({len(resume_text)} characters)")
                    
                    with st.expander("🔍 Preview Resume Text", expanded=False):
                        preview = resume_text[:300] + "..." if len(resume_text) > 300 else resume_text
                        # FIXED: Added proper label to avoid warning
                        st.text_area(
                            "Resume Preview", 
                            value=preview,
                            height=150,
                            disabled=True,
                            label_visibility="collapsed"
                        )
                        st.caption(f"Total characters: {len(resume_text)}")
                else:
                    st.error("Could not extract text from PDF. Please try another file.")
        else:
            st.info("📁 Please upload your resume in PDF format")
    
    with col2:
        st.markdown("### 💼 Job Details")
        
        job_title = st.text_input(
            "Target Job Title *",
            value=st.session_state.job_title,
            placeholder="e.g., Data Scientist, Software Engineer, Marketing Manager",
            help="Required for analysis"
        )
        st.session_state.job_title = job_title
        
        job_description = st.text_area(
            "Paste Job Description *",
            value=st.session_state.job_description,
            height=200,
            placeholder="Copy and paste the complete job description here...\n\nInclude:\n- Responsibilities\n- Requirements\n- Skills needed\n- Qualifications",
            help="Required for analysis"
        )
        st.session_state.job_description = job_description
        
        if job_description:
            word_count = len(job_description.split())
            char_count = len(job_description)
            st.caption(f"📝 Job Description: {word_count} words, {char_count} characters")
    
    # Analysis Button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_disabled = not st.session_state.resume_text
        analyze_btn = st.button(
            "🚀 START AI ANALYSIS",
            type="primary",
            use_container_width=True,
            disabled=analyze_disabled,
            help="Click to analyze your resume"
        )
    
    if analyze_disabled:
        st.warning("⚠️ Please upload a resume first")
    
    # Perform Analysis
    if analyze_btn:
        if not st.session_state.resume_text:
            st.error("Please upload a resume first")
        else:
            # Prepare analysis prompt
            analysis_prompt = f"""
            Analyze this resume for a {job_title} position:
            
            JOB DESCRIPTION:
            {job_description[:1000] if job_description else 'Not provided'}
            
            RESUME CONTENT:
            {st.session_state.resume_text[:2000]}
            
            Provide detailed analysis including:
            1. Match Score (0-100%)
            2. Key Strengths
            3. Areas for Improvement
            4. Missing Keywords
            5. Actionable Recommendations
            6. ATS Optimization Tips
            
            Format with clear headings and bullet points.
            Be specific and constructive.
            """
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Perform analysis based on selected mode
            try:
                if current_mode == "offline":
                    status_text.text("🔄 Running offline analysis...")
                    progress_bar.progress(30)
                    
                    result = offline_analyzer.analyze(
                        st.session_state.resume_text,
                        job_title,
                        job_description
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis complete!")
                    st.session_state.analysis_result = result
                
                else:
                    status_text.text(f"🔄 Connecting to {mode_name}...")
                    progress_bar.progress(20)
                    
                    result = online_analyzer.analyze_with_api(
                        analysis_prompt,
                        current_mode,
                        api_key if current_mode == "huggingface" else "",
                        selected_model
                    )
                    
                    progress_bar.progress(80)
                    
                    if "Error" in result or "unavailable" in result.lower():
                        status_text.text("⚠️ API failed, switching to offline analysis...")
                        result = offline_analyzer.analyze(
                            st.session_state.resume_text,
                            job_title,
                            job_description
                        )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis complete!")
                    st.session_state.analysis_result = result
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                result = offline_analyzer.analyze(
                    st.session_state.resume_text,
                    job_title,
                    job_description
                )
                st.session_state.analysis_result = result
    
    # Display Results
    if st.session_state.analysis_result:
        st.markdown("### 📊 Analysis Results")
        
        # Mode indicator
        mode_display = {
            "offline": "📴 Offline Analysis",
            "huggingface": "🤗 Hugging Face API",
            "openrouter": "🔄 OpenRouter API",
            "deepseek": "🔍 DeepSeek API"
        }
        
        st.caption(f"*Analysis Mode: {mode_display.get(current_mode, 'Unknown')} | Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # Results container
        st.markdown(f'<div class="result-box">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Download Report", use_container_width=True, help="Download analysis as text file"):
                report_text = f"""
                RESUME ANALYSIS REPORT
                ======================
                Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                Mode: {mode_display.get(current_mode, 'Unknown')}
                Job Title: {job_title}
                
                {st.session_state.analysis_result}
                """
                
                st.download_button(
                    label="Click to Download",
                    data=report_text,
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("🔄 Re-analyze", use_container_width=True, help="Run analysis again"):
                st.session_state.analysis_result = ""
                st.rerun()
        
        with col3:
            if st.button("⚙️ Change Mode", use_container_width=True, help="Try different analysis mode"):
                st.rerun()
        
        # Chat-like Q&A Section
        st.markdown("---")
        st.markdown("### 💬 Ask About Your Analysis")
        
        # Suggested questions
        st.markdown("**Quick Questions:**")
        q_col1, q_col2, q_col3 = st.columns(3)
        
        with q_col1:
            if st.button("How to improve score?", use_container_width=True):
                response = "To improve your match score, focus on adding missing keywords from the job description, quantifying achievements with specific numbers, and highlighting transferable skills."
                st.info(response)
        
        with q_col2:
            if st.button("Best format tips?", use_container_width=True):
                response = "Use a clean, professional template with clear sections. Ensure proper spacing, consistent fonts, and save as PDF. ATS-friendly resumes avoid tables and graphics."
                st.info(response)
        
        with q_col3:
            if st.button("Keyword strategy?", use_container_width=True):
                response = "Naturally integrate keywords in skills section, work experience, and summary. Use variations and synonyms. Avoid keyword stuffing which can hurt readability."
                st.info(response)
        
        # Custom question
        user_question = st.text_input(
            "Ask your own question:",
            placeholder="e.g., How can I highlight my leadership experience?"
        )
        
        if user_question:
            with st.spinner("🤔 Thinking..."):
                # Simple AI response based on question type
                if any(word in user_question.lower() for word in ["leadership", "manage", "team"]):
                    response = "For leadership experience: Use action verbs like 'Led', 'Managed', 'Directed'. Quantify team size, projects led, and results achieved. Example: 'Led a team of 5 developers to deliver project 2 weeks ahead of schedule.'"
                elif any(word in user_question.lower() for word in ["skill", "technical", "software"]):
                    response = "For skills section: List technical skills first, then soft skills. Use industry-standard terminology. Group related skills together. Consider a 'Core Competencies' section at the top."
                elif any(word in user_question.lower() for word in ["experience", "work", "job"]):
                    response = "For work experience: Use bullet points for each role. Start with action verbs. Include company name, job title, dates. Focus on achievements rather than duties. Quantify results with numbers."
                elif any(word in user_question.lower() for word in ["education", "degree", "certification"]):
                    response = "For education: List most recent degree first. Include institution, degree, graduation year. Add relevant coursework or honors. Include certifications with issuing organization and date."
                else:
                    response = "Based on your analysis, I recommend focusing on the specific recommendations provided. Tailor your resume for each job application, and always include quantifiable achievements."
                
                st.markdown(f"""
                <div class="tip-box">
                    <strong>🤖 AI Assistant:</strong><br>
                    {response}
                </div>
                """, unsafe_allow_html=True)

# ===============================
# Run Application
# ===============================
if __name__ == "__main__":
    main()