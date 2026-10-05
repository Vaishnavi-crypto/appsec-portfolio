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
    session["user_id"] = user[0]
    return redirect("/profile")
  return "User not found. <a href='/'>Go back</a>"


# SECURE ENDPOINT: Uses session state instead of user-supplied URL parameters
@app.route("/profile")
def profile():
  if "user_id" not in session:
    return redirect("/")

  # Fix: Fetch data strictly based on the verified session cookie, not URL input
  authenticated_user_id = session["user_id"]
  user_data = get_user_by_id(authenticated_user_id)

  if not user_data:
    return "Profile not found", 404

  return f"""
    <h2>User Profile (Secure)</h2>
    <p>Logged in securely as User ID: {authenticated_user_id}</p>
    <hr>
    <p>Username: {user_data['username']}</p>
    <p>Email: {user_data['email']}</p>
    <p>Credit Card: {user_data['credit_card']}</p>
    <p><em>Notice: You can no longer manipulate the URL to view other users' records.</em></p>
    <br><a href='/'>Logout / Home</a>
  """


@app.route("/")
def index():
  return """
    <h2>Login Simulation (Secure App)</h2>
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

  # Running on port 5001 so it doesn't conflict if your vulnerable app is on 5000
  app.run(debug=True, port=5001)