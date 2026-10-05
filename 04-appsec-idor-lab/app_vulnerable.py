from flask import Flask, redirect, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "super-secret-key-for-lab"


def get_user_by_id(user_id):
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT id, username, email, credit_card FROM users WHERE id = ?",
      (user_id,),
  )
  user = cursor.fetchone()
  conn.close()
  if user:
    return {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "credit_card": user[3],
    }
  return None


@app.route("/login", methods=["POST"])
def login():
  username = request.form.get("username")
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
  user = cursor.fetchone()
  conn.close()

  if user:
    session["user_id"] = user[0]  # Store logged-in user's ID
    return redirect(f"/profile?id={user[0]}")
  return "User not found. <a href='/'>Go back</a>"


# VULNERABLE ENDPOINT: Trusts the ?id= parameter completely
@app.route("/profile")
def profile():
  if "user_id" not in session:
    return redirect("/")

  user_id = request.args.get("id")
  user_data = get_user_by_id(user_id)

  if not user_data:
    return "Profile not found", 404

  # Flaw: No check to see if session['user_id'] matches user_id!
  return f"""
    <h2>User Profile (Vulnerable)</h2>
    <p>Logged in as User ID: {session['user_id']}</p>
    <hr>
    <h3>Viewing Profile for ID: {user_data['id']}</h3>
    <p>Username: {user_data['username']}</p>
    <p>Email: {user_data['email']}</p>
    <p>Credit Card: {user_data['credit_card']}</p>
    <br><a href='/profile?id=1'>View ID 1</a> | <a href='/profile?id=2'>View ID 2</a>
  """


@app.route("/")
def index():
  return """
    <h2>Login Simulation</h2>
    <form action='/login' method='POST'>
        Username (e.g., alice or bob): <input type='text' name='username'>
        <input type='submit' value='Login'>
    </form>
    """


if __name__ == "__main__":
  # Quick database setup for demo
  conn = sqlite3.connect("database.db")
  cursor = conn.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username"
      " TEXT, email TEXT, credit_card TEXT)"
  )
  cursor.execute("DELETE FROM users")
  cursor.executemany(
      "INSERT INTO users VALUES (?, ?, ?, ?)",
      [
          (1, "alice", "alice@example.com", "4111-xxxx-xxxx-1111"),
          (2, "bob", "bob@example.com", "4222-xxxx-xxxx-2222"),
      ],
  )
  conn.commit()
  conn.close()

  app.run(debug=True, port=5000)