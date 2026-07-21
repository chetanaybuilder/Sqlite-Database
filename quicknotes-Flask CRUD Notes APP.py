from flask import Flask,render_template,request,redirect
import sqlite3
app = Flask(__name__)
DATABASE="Quicknotes.db"
def get_db_connection():
   conn = sqlite3.connect(DATABASE)
   conn.row_factory = sqlite3.Row
   return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS notes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        content TEXT NOT NULL,

        user_id INTEGER,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )

    """)

    

    conn.commit()
    conn.close()
@app.route("/")
def home():
   return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
      email = request.form.get("email")
      password = request.form.get("password")

      conn = get_db_connection()
      cursor = conn.cursor()

      cursor.execute(
          "SELECT * FROM users WHERE email = ? AND password = ?",
          (email, password)
      )
      user = cursor.fetchone()
      conn.close()

      if user:
         return redirect("/notes")
      else:
         return "invalid credentials", 401

   return render_template("login.html")

 
@app.route("/register", methods=["GET", "POST"])
def register():
   if request.method == "POST":
      username = request.form.get("username")
      email = request.form.get("email")
      password = request.form.get("password")

      conn = get_db_connection()
      cursor = conn.cursor()

      cursor.execute(
          "INSERT INTO users(username,email,password) VALUES(?,?,?)",
          (username, email, password)
      )
      conn.commit()
      conn.close()

      return redirect("/notes")

   return render_template("register.html")

@app.route("/notes", methods=["GET", "POST"])
def notes():
   if request.method == "POST":
      title = request.form.get("title")
      content = request.form.get("content")

      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO notes(title,content,user_id) VALUES(?,?,?)",
          (title, content,1)
      )
      conn.commit()
      conn.close()

      return "Note Saved Successfully"

   conn = get_db_connection()
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM notes")
   notes = cursor.fetchall()

   conn.close()
   return render_template("notes.html", notes=notes)

if __name__ == "__main__":
   create_tables()
   app.run(debug=True)