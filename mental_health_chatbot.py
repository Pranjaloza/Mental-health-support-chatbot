import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch
import random
import sqlite3

# Load dataset
df = pd.read_csv("mental_health_chatbot.csv")
df[['question', 'answer']] = df['text'].str.extract(r'<HUMAN>:\s*(.*?)\s*<ASSISTANT>:\s*(.*)')
df = df[df['answer'].str.len() > 30].dropna()

questions = df['question'].tolist()
answers = df['answer'].tolist()

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = model.encode(questions, convert_to_tensor=True)

# Connect to SQLite DB
conn = sqlite3.connect('chat_logs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chatlog (session_id TEXT, user_input TEXT, bot_response TEXT)''')
conn.commit()

# Streamlit app config
st.set_page_config(page_title="Mental Health Chatbot", page_icon="💙", layout="centered")

# Custom style
st.markdown("""
    <style>
    html, body, [class*="css"]  { font-family: 'Segoe UI', sans-serif; }
    .chat-bubble { padding: 0.8rem; margin: 0.5rem 0; border-radius: 12px; }
    .user-bubble { background-color: #e3f2fd; color: #0d47a1; text-align: left; }
    .bot-bubble { background-color: #e8f5e9; color: #2e7d32; text-align: left; }
    .stTextInput>div>div>input { padding: 0.6rem; border-radius: 8px; }
    .stButton>button { background-color: #1976d2; color: white; font-weight: bold; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(random.randint(1000, 9999))

st.title("💬 Mental Health Chatbot")

# Clear chat button
if st.button("🧹 New Session"):
    st.session_state['history'] = []
    st.session_state['session_id'] = str(random.randint(1000, 9999))

# Profanity filter
def contains_profanity(text):
    bad_words = ["damn", "shit", "fuck", "asshole", "bitch"]  # extend if needed
    return any(bad in text.lower() for bad in bad_words)

# Text input
user_input = st.text_input("How are you feeling today?", key="input")

if user_input:
    crisis_words = [
        "suicide", "kill myself", "want to die", "hopeless",
        "I want to end it", "not worth living"
    ]

    greetings = ['hello', 'hi', 'hey', 'good morning', 'good evening']

    emojis_only = all(char in '😀😃😄😁😅😂🤣😊😇🙂🙃😉😍😘😗😙😚😋😜😝😭😢😡😠🤬😤' for char in user_input if not char.isspace())

    if emojis_only:
        response = "I noticed you're expressing strong feelings. I'm here for you 💙"

    elif contains_profanity(user_input):
        response = "Let's try to keep this space positive and supportive. I'm here to listen."

    elif any(word in user_input.lower() for word in crisis_words):
        response = "⚠️ You're not alone. Please contact a mental health helpline near you. You are important and valued."

    elif user_input.lower() in greetings:
        response = random.choice([
            "Hi there! I'm here for you. How are you feeling today?",
            "Hello! I'm here to listen. What’s on your mind?",
            "Hey there! How can I support you today?"
        ])

    else:
        query_embedding = model.encode(user_input, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=5)

        skip_phrases = ["goodbye", "see you", "take care", "have a nice", "bye"]

        good_responses = []
        for idx in top_results.indices:
            answer = answers[idx].strip()
            word_count = len(answer.split())
            if (
                word_count >= 20
                and not any(skip in answer.lower() for skip in skip_phrases)
            ):
                good_responses.append(answer)

        if good_responses:
            selected = random.choice(good_responses)
            starter = random.choice([
                "Thanks for sharing. Here's a thought:",
                "You're not alone. Here's some insight:",
                "I understand. Take a look at this:"
            ])
            response = f"{starter}\n\n{selected}"
        else:
            response = "I'm here for you, even if I don't have the perfect words right now. You're not alone."

    # Save to chat history + SQLite
    st.session_state['history'].append((user_input, response))
    c.execute("INSERT INTO chatlog VALUES (?, ?, ?)", (st.session_state['session_id'], user_input, response))
    conn.commit()

# Display chat history
st.markdown("---")
for user, bot in st.session_state['history']:
    st.markdown(f"<div class='chat-bubble user-bubble'><b>You:</b> {user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble bot-bubble'><b>Bot:</b> {bot}</div>", unsafe_allow_html=True)
