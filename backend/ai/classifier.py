import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_issue(description):
    prompt = f"""
    You are an AI system for a campus maintenance app.

    Classify the issue below.

    Issue:
    {description}

    Rules:
    - Category must be ONE of:
    Electrical, Plumbing, Cleaning, Internet, Furniture, Other
    - Priority must be ONE of:
    Low, Medium, High
    - Respond in EXACT format below
    - No explanations

    Format:
    Category: <category>
    Priority: <priority>
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You classify campus maintenance issues."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        text = response.choices[0].message.content.strip()
        print("GROQ RAW RESPONSE:", text)

        category = "Other"
        priority = "Medium"

        for line in text.splitlines():
            if line.startswith("Category:"):
                category = line.replace("Category:", "").strip()
            if line.startswith("Priority:"):
                priority = line.replace("Priority:", "").strip()

        return category, priority

    except Exception as e:
        print("GROQ ERROR:", e)
        return "Other", "Medium"