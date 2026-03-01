import os
import requests
from typing import Literal
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
DEALS_BOARD_ID = "5026874399"
WORK_ORDERS_BOARD_ID = "5026874265"

@tool
def query_monday_board(board_name: Literal["deals", "work_orders"]):
    """
    Fetches live data from specific monday.com boards.
    - Use 'deals' for sales pipeline, deal values, stages, and sector-wise revenue analysis.
    - Use 'work_orders' for project execution status, billing, and actual collections data.
    """

    if board_name == "deals":
        board_id = DEALS_BOARD_ID
    else:
        board_id = WORK_ORDERS_BOARD_ID

    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": MONDAY_API_KEY,
        "API-Version": "2024-04",
        "Content-Type": "application/json"
    }

    query = f"""
    query {{
      boards (ids: {board_id}) {{
        name
        items_page (limit: 30) {{
          items {{
            name
            column_values {{
              id
              text
            }}
          }}
        }}
      }}
    }}
    """
    
    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if "errors" in data:
            return f"Monday.com API Error: {data['errors'][0]['message']}"
            
        return data
        
    except requests.exceptions.RequestException as e:
        return f"Network error connecting to monday.com: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"