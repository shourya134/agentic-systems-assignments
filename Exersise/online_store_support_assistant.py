from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent  
from langchain_core.output_parsers import StrOutputParser

orders_db={
    "12345": {
        "status": "Shipped",
        "estimated_delivery": "2024-06-15",
        "amount": "$150.00"
    },
    "21223": {
        "status": "cancelled",
        "estimated_delivery": "N/A",
        "amount": "$200.00"
    },
    "12335": {
        "status": "Delivered",
        "estimated_delivery": "2024-06-10",
        "amount": "$100.00"
    }
    
}

@tool
def get_order_status(product_id: str):
    """
    Get order status by product ID.
    """
    # Here you would implement the logic to retrieve order status from your database or API.
    # For demonstration purposes, we'll return a mock response.

    product_details = orders_db.get(product_id, {"status": "Not Found", "estimated_delivery": "N/A"})
    if product_details["status"] == "Not Found":
        return f"Order with product ID {product_id} not found."
    return f"Order Status: {product_details['status']}"
    
@tool
def get_estimated_delivery(product_id: str):
    """
    Get estimated delivery date by product ID.
    """
    product_details = orders_db.get(product_id, {"status": "Not Found", "estimated_delivery": "N/A"})
    if product_details["status"] == "Not Found":
        return f"Order with product ID {product_id} not found."
    return f"Estimated Delivery Date: {product_details['estimated_delivery']}"  

@tool
def calculate_refund_amount(product_id:str):
    """
    Calculate refund amount if the order was cancelled
    """
    product_details = orders_db.get(product_id, {"status": "Not Found", "amount": "N/A"})
    if product_details["status"] == "Not Found":
        return f"Order with product ID {product_id} not found."
    if product_details["status"].lower() == "cancelled":
        return f"Refund Amount: {product_details['amount']}"
    else:
        return f"No refund applicable. Order status is '{product_details['status']}'."


tools = [get_order_status, get_estimated_delivery, calculate_refund_amount]

llm = ChatOllama(model="gemma4:latest", temperature=0)

agent = create_agent(llm,tools)

messages = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful ecommerece agent, use tools when required"),
    ("user","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

from langchain_core.messages import HumanMessage

result = agent.invoke({"messages": [HumanMessage(content="where is my order 12345")]})
parser = StrOutputParser()
print(result['messages'][-1].content)

