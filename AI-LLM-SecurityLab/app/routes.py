from flask import Blueprint, render_template, request, jsonify

from app.llm import generate_response

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")

    user_id = data.get("user_id", "UNKNOWN")
    response = generate_response(message, user_id)
    return jsonify({
        "response": response
    })