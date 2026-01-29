import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API')
genai.configure(api_key=GEMINI_API_KEY)

# --- 1. LOAD DATABASE FILES ---
# We use relative paths to go up one level (..) to find 'Database'
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, '..', 'Database')

def load_json(filename):
    try:
        path = os.path.join(db_dir, filename)
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading {filename}: {e}")
        return []

# Load data into memory once when script starts
products = load_json('product_catalog.json')
orders = load_json('order_database.json')
faqs = load_json('product_faqs.json')

# --- 2. DEFINE TOOLS (The Logic) ---

def search_products(query):
    """Searches product catalog for price, stock, and details."""
    query = query.lower()
    results = []
    
    # Simple keyword search
    for p in products:
        # Adjust keys based on your actual JSON structure (e.g., 'name', 'title')
        p_str = str(p).lower() 
        if query in p_str:
            results.append(p)
            
    if not results:
        return "No matching products found."
    
    return json.dumps(results[:3]) # Limit to top 3 to keep it short

def check_order(order_id):
    """Checks status of a specific order ID."""
    # Strip "ORD-" or "Order" to just get numbers if needed
    clean_id = str(order_id).replace("ORD-", "").strip()
    
    for o in orders:
        # Check against your JSON key (e.g., 'id', 'order_id')
        if str(o.get('order_id', '')).endswith(clean_id):
            return json.dumps(o)
            
    return "Order ID not found."

def get_policy_answer(query):
    """Looks up FAQ/Policies."""
    # (Simple Keyword Match for now)
    for q in faqs:
        if query.lower() in q.get('question', '').lower():
            return q.get('answer')
    return None

# --- 3. CONFIGURE GEMINI WITH TOOLS ---
tools = [search_products, check_order]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools,
    system_instruction="""
    You are a store assistant. 
    1. Use the available tools to look up real data.
    2. If a user asks about a product, call search_products.
    3. If a user asks about an order, call check_order.
    4. Keep answers spoken-word friendly (short, no markdown).
    """
)

chat = model.start_chat(enable_automatic_function_calling=True)

# --- MAIN ENTRY POINT ---
def process_user_input(text):
    try:
        print(f"🧠 Thinking about: {text}")
        response = chat.send_message(text)
        return response.text.replace("*", "") # Clean up text for TTS
    except Exception as e:
        print(f"❌ Brain Error: {e}")
        return "I'm having trouble accessing the database right now."