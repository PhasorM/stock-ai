import os
import json
from thefuzz import process, fuzz

def search_products(query):
    """Searches product catalog using fuzzy matching to handle STT typos."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Database', 'product_catalog.json')
    
    try:
        with open(db_path, 'r') as f:
            products = json.load(f)
        
        if not products:
            return "The product catalog is currently empty."

        # 1. Create a list of just the names/titles to search against
        # Note: Ensure your JSON uses the key 'name' or change it below
        product_names = [p.get('name', 'Unknown Product') for p in products]

        # 2. Extract top matches using 'partial_ratio' 
        # (Better for finding 'Sony' in 'Sony WH-1000XM4')
        matches = process.extract(query, product_names, limit=3, scorer=fuzz.partial_ratio)

        # 3. Filter results based on a threshold (e.g., 65/100)
        final_results = []
        for match_name, score in matches:
            if score >= 65:
                # Find the full product dictionary that matches this name
                product_obj = next((p for p in products if p.get('name') == match_name), None)
                if product_obj:
                    # Optional: Attach the score so Gemini knows the confidence level
                    product_obj['match_confidence'] = f"{score}%"
                    final_results.append(product_obj)

        if not final_results:
            return f"I couldn't find any products matching '{query}'."

        return json.dumps(final_results)

    except Exception as e:
        return f"Database access error: {str(e)}"