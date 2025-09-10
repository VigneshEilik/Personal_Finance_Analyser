import os
import streamlit as st
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key securely
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=gemini_api_key)


# Streamlit UI
st.set_page_config(page_title="Finance Assistant", layout="wide")

# Background Image CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/premium-photo/glowing-white-stock-market-chart-dark-background-chart-is-made-up-lines-bars-which-represent-prices-stocks-time_14117-213756.jpg?w=2000");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);  /* transparent header */
}
[data-testid="stToolbar"] { 
    right: 2rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("💰 AI-Powered Personal Finance Assistant")

# Custom CSS for Styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        color: #4CAF50;
        text-shadow: 2px 2px 5px rgba(76, 175, 80, 0.4);
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #ddd;
        margin-bottom: 20px;
    }
    .stButton button {
        background: linear-gradient(to right, #4CAF50, #388E3C);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(to right, #388E3C, #2E7D32);
    }
    .result-card {
        background: rgba(0, 150, 136, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(0, 150, 136, 0.2);
    }
    .success-banner {
        background: linear-gradient(to right, #2E7D32, #1B5E20);
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 2px 8px rgba(0, 150, 136, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# # Sidebar with usage info
# st.sidebar.title("ℹ️ How to Use This Tool?")
# st.sidebar.write("- Upload your Paytm Transaction History PDF.")
# st.sidebar.write("- The AI will analyze your transactions.")
# st.sidebar.write("- You will receive financial insights including income, expenses, savings, and spending trends.")
# st.sidebar.write("- Use this data to plan your finances effectively.")

# st.markdown('<h1 class="main-title">💰 AI-Powered Personal Finance Assistant</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub-title">Upload your Paytm Transaction History PDF for Financial Insights</p>', unsafe_allow_html=True)

# Upload PDF File
uploaded_file = st.file_uploader("📂 Upload PDF File", type=["pdf"])

def extract_text_from_pdf(file_path):
    """Extracts text from the uploaded PDF file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_financial_data(text):
    """Sends extracted text to Google Gemini AI for financial insights."""
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    prompt = f"""
    Analyze the following Paytm transaction history and generate financial insights:
    {text}

    Provide a detailed breakdown in the following format:

    **Financial Insights for [User Name]**

    **Key Details:**

    - **Overall Monthly Income & Expenses:**
      - Month: [Month]
      - Income: ₹[Amount]
      - Expenses: ₹[Amount]

    - **Unnecessary Expenses Analysis:**
      - Expense Category: [Category Name]
      - Amount: ₹[Amount]
      - Recommendation: [Suggestion]

    - **Savings Percentage Calculation:**
      - Savings Percentage: [Percentage] %

    - **Expense Trend Analysis:**
      - Notable Trends: [Trend Details]

    - **Cost Control Recommendations:**
      - Suggestion: [Detailed Suggestion]

    - **Category-Wise Spending Breakdown:**
      - Category: [Category Name] - ₹[Amount]
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Error processing financial data."

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from document..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ Failed to extract text. Ensure the document is not a scanned image PDF.")
    else:
        progress_bar = st.progress(0)
        with st.spinner("🤖 AI is analyzing your financial data"):
            insights = analyze_financial_data(extracted_text)

        progress_bar.progress(100)

        st.subheader("📊 Financial Insights Report")
        st.markdown(f'<div class="result-card"><b>📄 Financial Report for {uploaded_file.name}</b></div>', unsafe_allow_html=True)

        st.write(insights)

        st.markdown('<div class="success-banner">⭐️ Plan your future finances wisely ⭐️</div>', unsafe_allow_html=True)

        # Custom HTML + CSS for falling dollars
        dollar_animation = """
        <style>
        @keyframes fall {
        0% { transform: translateY(-10vh); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
        }
        .dollar {
        position: fixed;
        top: 0;
        left: 50%;
        font-size: 2rem;
        animation: fall 3s linear infinite;
        }
        </style>
        <div class="dollar">💲</div>
        <div class="dollar" style="left:20%; animation-delay: 0.5s;">💲</div>
        <div class="dollar" style="left:70%; animation-delay: 1s;">💲</div>
        <div class="dollar" style="left:40%; animation-delay: 0.5s;">💲</div>
        <div class="dollar" style="left:60%; animation-delay: 1s;">💲</div>
        <div class="dollar" style="left:20%; animation-delay: 0.5s;">💲</div>
        <div class="dollar" style="left:40%; animation-delay: 1.5s;">💲</div>
        <div class="dollar" style="left:80%; animation-delay: 0.5s;">💲</div>
        <div class="dollar" style="left:30%; animation-delay: 0.5s;">💲</div>
        <div class="dollar" style="left:90%; animation-delay: 0.5s;">💲</div>
        """

        st.markdown(dollar_animation, unsafe_allow_html=True)

    os.remove(file_path)  # Cleanup

