import os
import json

def check_order(order_id):
    """Checks status of a specific order ID."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'Database', 'order_database.json')
    try:
        with open(db_path, 'r') as f:
            orders = json.load(f)
        
        clean_id = str(order_id).replace("ORD-", "").strip()
        for o in orders:
            if str(o.get('order_id', '')).endswith(clean_id):
                return json.dumps(o)
        return "Order ID not found."
    except Exception as e:
        return f"Error accessing order database: {e}"