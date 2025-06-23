# 🩵 Mental Health Support Chatbot

An AI-powered mental health conversational chatbot built using **Streamlit** and **Sentence Transformers**. This chatbot provides empathetic support, responds to emotional conversations, and recommends thoughtful replies based on semantic similarity with a curated mental health dialogue dataset.

---

## 📌 Features

- Emotionally supportive mental health chatbot
- Uses pre-trained `all-MiniLM-L6-v2` Sentence Transformer for semantic search
- Detects crisis phrases and gives sensitive responses
- Basic profanity filter to keep conversations respectful
- Stores chat logs using SQLite for session history
- Simple and clean UI using Streamlit
- ✅ **Deployed on Streamlit Cloud**

---

## 🌐 Live Demo

🚀 **([Click here to try it live on Streamlit Cloud]**(https://mentalhealthchatbot-65rjzfdlpbvfhmbhmd24kj.streamlit.app/))

---
---

## 🖥️ Local Installation & Run

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mental-health-chatbot.git
cd mental-health-chatbot

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run mental_health_chatbot.py
```

---

## 🗃️ Dataset
The dataset contains real-world supportive conversations, formatted like:

 <HUMAN>: I'm feeling down.

 <ASSISTANT>: I'm really sorry to hear that. You're not alone—I'm here for you.

Only answers longer than 30 characters are used to ensure meaningful responses.
---

---
## 🧠 Technologies Used

- sentence-transformers for semantic similarity
- streamlit for UI and app hosting
- torch for tensor-based similarity calculations
- sqlite3 for simple backend storage of chat logs
---

---

## 📬 Contact
Built with 💙 by Pranjal Oza

📧 Reach out for suggestions 
