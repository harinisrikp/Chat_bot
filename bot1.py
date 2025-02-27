import streamlit as st
import requests
from groq import Groq
from textblob import TextBlob

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #2E3B4E;
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    padding: 20px;
    color: white;
}

h1, h2, h3 {
    color: #ffcc00;
    text-align: center;
}

.chat-input-container {
    background-color: #2E3B4E;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
}

[data-testid="stChatInput"] textarea {
    border-radius: 10px;
    padding: 20px;
    color: white;
    font-size: 18px;
    height: 80px;
    background-color: #3A4A68;
    border: 2px solid rgba(255, 255, 255, 0.8);
}

textarea::placeholder {
    color: white !important;
}

[data-testid="stSidebar"] {
    background-color: #3A4A68;
    color: white;
}
[data-testid="stSidebar"] .css-1d391kg {
    background-color:#0F2E5D; 
    color: white;  
}

.stButton button {
    color: white !important;
}
</style>
"""

def load_css():
    st.markdown(page_bg_img, unsafe_allow_html=True)
c
load_css()

if "show_menu" not in st.session_state:
    st.session_state.show_menu = False
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "bot_response" not in st.session_state:
    st.session_state.bot_response = None

def add_to_history(user_input, model_response):
    st.session_state.conversation_history.append(
        {"user": user_input, "response": model_response}
    )

def format_conversation_history():
    formatted_history = ""
    for entry in st.session_state.conversation_history:
        formatted_history += f"User: {entry['user']}\nBot: {entry['response']}\n"
    return formatted_history

MAX_TOKENS = 2048

def get_limited_context():
    context = format_conversation_history()
    tokens = context.split()
    if len(tokens) > MAX_TOKENS:
        context = " ".join(tokens[-MAX_TOKENS:])
    return context

def correct_spelling(user_input):
    blob = TextBlob(user_input)
    corrected_input = blob.correct()
    return str(corrected_input)

def generate_response(user_input, client):
    user_input = correct_spelling(user_input)
    context = get_limited_context()
    prompt = f"""
    You are an expert AI chatbot specialized in providing clear, medically accurate, and patient-friendly explanations about cervical cancer, its symptoms, diagnosis, treatment, and prevention.
    
    Keep responses concise, informative, and jargon-free where possible.
    
    Conversation history:
    {context}
    
    User: {user_input}
    Bot:
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",  
        )
        model_response = chat_completion.choices[0].message.content
    except Exception as e:
        model_response = f"Error generating response: {str(e)}"
    
    add_to_history(user_input, model_response)
    return model_response

client = Groq(api_key="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")

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("🔬 Cervical Cancer Chat Assistant")
st.markdown("#### Ask about symptoms, risk factors, tests, treatments & more!")

if st.button("☰ Menu", key="menu_icon", help="Show Menu"):
    st.session_state.show_menu = not st.session_state.show_menu

if st.session_state.show_menu:
    st.sidebar.title("Menu")
    if st.sidebar.button("📝 Show History"):
        st.session_state.show_history = not st.session_state.show_history
    if st.sidebar.button("🔄 New Chat"):
        st.session_state.conversation_history = []
        st.session_state.show_history = False

if st.session_state.show_history:
    st.sidebar.write("### Conversation History")
    if st.session_state.conversation_history:
        for entry in st.session_state.conversation_history:
            st.sidebar.write(f"**User:** {entry['user']}")
            st.sidebar.write(f"**Bot:** {entry['response']}")
            st.sidebar.write("---")
    else:
        st.sidebar.write("No conversation history available.")

with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.chat_input("Enter your prompt here:")
    st.markdown('</div>', unsafe_allow_html=True)

response = None

if user_input:
    with st.spinner("🤖 Thinking..."):
        response = generate_response(user_input, client)

if response:
    st.markdown(f'<div class="chat-message"><span class="user-message">👤 User:</span> {user_input}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-message"><span class="bot-message">🤖 Bot:</span> {response}</div>', unsafe_allow_html=True)
