from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from services.firestore_service import add_issue, get_all_issues, update_issue_status
from datetime import datetime
from ai.classifier import classify_issue
import os

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5500",
                "https://*.vercel.app",
                "https://campussuite-backend-a7mx.onrender.com"
            ]
        }
    },
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.route("/")
def home():
    return "Smart Campus Backend Running"

@app.route("/issue", methods=["POST", "OPTIONS"])
def create_issue():
    if request.method == "OPTIONS":
        response = jsonify({"ok": True})
        response.headers.add(
            "Access-Control-Allow-Origin",
            request.headers.get("Origin", "*")
        )
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json(silent=True) or {}

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
    issues = get_all_issues()
    return jsonify(issues)

@app.route("/admin/issue/<issue_id>", methods=["PATCH"])
def update_issue(issue_id):
    data = request.json
    new_status = data.get("status")

    if new_status not in ["Pending", "In Progress", "Resolved"]:
        return jsonify({"error": "Invalid status"}), 400

    update_issue_status(issue_id, new_status)
    return jsonify({"message": "Issue status updated"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
