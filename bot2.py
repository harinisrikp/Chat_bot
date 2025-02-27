import streamlit as st
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
    font-family: 'Arial', sans-serif;
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

.stButton button {
    color: white !important;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def add_to_history(user_input, model_response):
    st.session_state.conversation_history.append({"user": user_input, "response": model_response})

def format_conversation_history():
    return "\n".join(f"User: {entry['user']}\nBot: {entry['response']}" for entry in st.session_state.conversation_history)

def correct_spelling(user_input):
    return str(TextBlob(user_input).correct())

def generate_response(user_input, client):
    user_input = correct_spelling(user_input)
    context = format_conversation_history()
    prompt = f"""
    You are an expert AI chatbot providing precise, medically accurate, and easy-to-understand explanations about cervical cancer.
    
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

st.title("🔬 Cervical Cancer AI Assistant")
st.markdown("#### Get expert insights on cervical cancer, symptoms, and prevention.")

with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.chat_input("Enter your prompt here:")
    st.markdown('</div>', unsafe_allow_html=True)

if user_input:
    with st.spinner("Generating response..."):
        response = generate_response(user_input, client)
    st.markdown(f"**User:** {user_input}")
    st.markdown(f"**Bot:** {response}")
