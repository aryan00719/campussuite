import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------
# Firebase Initialization
# -------------------------------

FIREBASE_KEY = os.getenv("FIREBASE_KEY")

if not FIREBASE_KEY:
    raise RuntimeError(
        "FIREBASE_KEY environment variable not set. "
        "Paste full Firebase service account JSON into env var."
    )

# Parse Firebase JSON from env var
try:
    firebase_cred = json.loads(FIREBASE_KEY)
except json.JSONDecodeError:
    raise RuntimeError("FIREBASE_KEY is not valid JSON")

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# -------------------------------
# Firestore Operations
# -------------------------------

def add_issue(issue_data: dict):
    """Add a new issue document to Firestore"""
    db.collection("issues").add(issue_data)


def get_all_issues():
    """Fetch all issues from Firestore"""
    docs = db.collection("issues").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]


def update_issue_status(issue_id: str, status: str):
    """Update status of an issue"""
    db.collection("issues").document(issue_id).update({
        "status": status
    })