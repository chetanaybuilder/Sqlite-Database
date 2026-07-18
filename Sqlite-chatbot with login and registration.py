from google import genai
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Keep your exact API key setup
client = genai.Client(api_key="YOUR_API_KEY_HERE") 

app = Flask(__name__)
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = conn.cursor()

# Your exact table setup
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_message TEXT,
bot_response TEXT)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
password TEXT NOT NULL)
""")
conn.commit()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat", methods=["GET", "POST"])
def index():
    response = ""
    rows = []
    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            # Your exact Gemini call
            result = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""You are Chetanay AI.
                
                Rules:
                - Answer in this exact format.
                - Start with a relevant emoji.
                - Use 2-5 relevant emojis naturally.
                - Keep answers under 100 words.
                - Never use Markdown.
                - Never use ***, **, or *.
                - Never write long paragraphs.
                - Use a short title.
                - Then give 3-5 numbered points.
                - Each point must be one short sentence.
                - End with a one-line summary.
                
                {user_message}"""
            )
            
            bot_reply = getattr(result, "text", None) or str(result)
            
            cursor.execute("""
            INSERT INTO messages(user_message,bot_response)
            VALUES(?,?)
            """, (user_message, bot_reply))
            conn.commit()
            response = bot_reply
            
    cursor.execute("SELECT * FROM messages ORDER BY id")
    rows = cursor.fetchall()
    return render_template("index.html", response=response, chat_history=rows)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        print(username)
        print(email)
        print(password)
        
        try:
            cursor.execute("""
                INSERT INTO users(username,email,password) VALUES(?,?,?)""",
                (username, email, password)
            )
            conn.commit()
            
            # 👇 THIS IS THE ONLY LINE I ADDED 👇
            # After successful registration, push them to the login page!
            return redirect(url_for("login")) 
            
        except sqlite3.IntegrityError:
            # ignore duplicate email for simplicity
            pass
            
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        cursor.execute("""
            SELECT * FROM users WHERE email=? AND password=?""",
            (email, password)
        )
        
        user = cursor.fetchone()
        
        if user:
            # Your code was already correct here! 
            # It redirects to the '/chat' route because the function is named 'index'
            return redirect(url_for("index"))
        else:
            return "Invalid Email or Password"
            
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
    conn.close()