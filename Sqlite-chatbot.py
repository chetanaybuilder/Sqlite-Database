from google import genai
from flask import Flask, render_template, request
import sqlite3
client = genai.Client(api_key="paste_your_key_here")

app = Flask(__name__)
conn = sqlite3.connect("chatbot.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_message TEXT,
bot_response TEXT)
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    rows = cursor.fetchall()
    if request.method == "POST":
        user_message = request.form.get("message", "")
        
        # 1. Make the API call first to get the 'result'
        result = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are Chetanay AI.

You are Chetanay AI.

Rules:
- Answer in this exact format.
- Start with a relevant emoji.
- Use 2-5 relevant emojis naturally (🤖 🚀 📌 💡 ⚡ ✅ ❌ 📚).
- Keep answers under 100 words.
- Never use Markdown.
- Never use ###, **, or *.
- Never write long paragraphs.
- Use a short title.
- Then give 3-5 numbered points.
- Each point must be one short sentence.
- End with a one-line summary.

Example:

🐍 Python

1. 📖 Python is easy to learn.
2. 🤖 It is used for AI and machine learning.
3. 🌐 It builds websites and APIs.
4. ⚙️ It automates repetitive tasks.

💡 Summary:
Python is a beginner-friendly language used in many industries.

{user_message}
"""
        )
        
        
        bot_reply = result.text

        cursor.execute("""
        INSERT INTO messages(user_message,bot_response)
        values(?,?)
        """, (user_message,bot_reply))
        cursor.execute("SELECT*FROM messages")
        response = bot_reply
        conn.commit()
        
    return render_template("index.html", response=response, chat_history=rows)

if __name__ == "__main__":
    app.run(debug=True)
    conn.close()