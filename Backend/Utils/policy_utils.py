import os
import json

def get_policy_answer(query):
    """Looks up FAQ/Policies."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Database', 'product_faqs.json')
    try:
        with open(db_path, 'r') as f:
            faqs = json.load(f)
        
        for q in faqs:
            if query.lower() in q.get('question', '').lower():
                return q.get('answer')
        return "I couldn't find a specific policy regarding that."
    except Exception as e:
        return f"Error accessing policy database: {e}"