import os
import google.generativeai as genai
from dotenv import load_dotenv

# Import your new utilities
from Utils.product_utils import search_products
from Utils.order_utils import check_order
from Utils.policy_utils import get_policy_answer

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API'))

# List the functions for Gemini to use
tools = [search_products, check_order, get_policy_answer]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools,
    system_instruction="""
    You are a professional store assistant. 
    - Use 'search_products' for inventory/price questions.
    - Use 'check_order' for order status updates.
    - Use 'get_policy_answer' for general FAQs or store policies.
    - Be concise and friendly.
    """
)

chat = model.start_chat(enable_automatic_function_calling=True)

def process_user_input(text):
    try:
        response = chat.send_message(text)
        return response.text.replace("*", "") 
    except Exception as e:
        print(f"❌ Brain Error: {e}")
        return "I'm having trouble thinking right now."