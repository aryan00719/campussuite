from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from services.firestore_service import add_issue, get_all_issues, update_issue_status
from datetime import datetime
from ai.classifier import classify_issue
import os

app = Flask(__name__)

# ✅ SIMPLE + CORRECT CORS (Hackathon Safe)
CORS(
    app,
    supports_credentials=False,
    resources={r"/*": {"origins": "*"}},
)

@app.route("/")
def home():
    return "Smart Campus Backend Running"

@app.route("/issue", methods=["POST"])
def create_issue():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    description = data.get("description")
    location = data.get("location")

    if not description or not location:
        return jsonify({"error": "Missing description or location"}), 400

    category, priority = classify_issue(description)

    issue = {
        "user_id": data.get("user_id", "demo_user"),
        "description": description,
        "location": location,
        "category": category,
        "priority": priority,
        "status": "Pending",
        "created_at": datetime.utcnow()
    }

    add_issue(issue)

    return jsonify({
        "message": "Issue submitted successfully",
        "category": category,
        "priority": priority
    }), 200

@app.route("/admin/issues", methods=["GET"])
def get_issues():
    return jsonify(get_all_issues())

@app.route("/admin/issue/<issue_id>", methods=["PATCH"])
def update_issue(issue_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Pending", "In Progress", "Resolved"]:
        return jsonify({"error": "Invalid status"}), 400

    update_issue_status(issue_id, new_status)
    return jsonify({"message": "Issue status updated"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)