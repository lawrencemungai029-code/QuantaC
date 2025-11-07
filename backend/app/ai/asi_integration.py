import requests
from ..config import ASI_ENDPOINT, ASI_API_KEY

ASI_PROMPT = '''Instruction:
You are ASI1. Given the "content" field below (HTML or text of a web page or event description), extract human-readable, canonical opportunity objects. Return a JSON array of objects. Each object must include the keys:

- title (string or null)
- organization (string or null)
- type (one of: "Hackathon","Internship","Freelance","Competition","Training","Other" or null)
- category (string or null)
- description (string or null) -- concise cleaned summary (max 300 words)
- skills (array of strings, normalized to lowercase hyphenated phrases e.g., "machine-learning")
- deadline (ISO 8601 date-time string, or null)
- posted_date (ISO 8601 date-time string, or null)
- location (string or "Remote")
- link (string - canonical applying link or null)
- source_url (string - the original page URL)
- is_ai_generated (boolean - set true)
- date_scraped (ISO 8601)
- confidence_score (float, 0.0 - 1.0)
- raw_payload (string - short snippet or original text)

If any value is unknown, put null. Output must be valid JSON and nothing else.'''

def extract_opportunities_from_text(raw_text):
    payload = {
        "task": "extract_opportunity_fields",
        "content": raw_text,
        "instructions": ASI_PROMPT
    }
    headers = {"Authorization": f"Bearer {ASI_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(ASI_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def get_embedding(text):
    payload = {"task": "embedding", "text": text}
    headers = {"Authorization": f"Bearer {ASI_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(f"{ASI_ENDPOINT}/embeddings", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
