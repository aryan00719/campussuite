import os
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------
# Firebase Initialization
# -------------------------------

# Get Firebase key path from environment variable
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY")

if not FIREBASE_KEY_PATH:
    raise RuntimeError(
        "FIREBASE_KEY environment variable not set. "
        "Please set it in .env file."
    )

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# -------------------------------
# Firestore Operations
# -------------------------------

def add_issue(issue_data: dict):
    """
    Add a new issue document to Firestore
    """
    db.collection("issues").add(issue_data)


def get_all_issues():
    """
    Fetch all issues from Firestore
    """
    docs = db.collection("issues").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]


def update_issue_status(issue_id: str, status: str):
    """
    Update status of an issue (Open / Verified / Resolved)
    """
    db.collection("issues").document(issue_id).update({
        "status": status
    })