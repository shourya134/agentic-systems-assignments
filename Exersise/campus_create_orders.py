import json
import os

from langchain_ollama import ChatOllama
from langchain.messages import ToolMessage, SystemMessage, HumanMessage
from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser


ORDERS_DB = {
    "CC2001": {
        "order_id": "CC2001",
        "item": "Hoodie — Batch 2026",
        "status": "shipped",
        "eta_days": 3,
    },
}


# TODO 1: Define OrderStatusInput (Pydantic)
class OrderStatusInput(BaseModel):
    order_id: str = Field(..., description="The ID of the order to check status for.")


# TODO 2: Define get_order_status with @tool
@tool(args_schema=OrderStatusInput)
def get_order_status(input: OrderStatusInput) -> str:
    """
    Get the status of an order by its ID. Use where the order_id is the input.order_id to look up the order in ORDERS_DB. If the order is found, return a JSON string with "ok": True and the order details. If not found, return a JSON string with "ok": False and an error message.
    """
    order_id = input.order_id.strip().upper()
    order = ORDERS_DB.get(order_id)
    if not order:
        return json.dumps({"ok": False, "message": "Order not found."})
    return json.dumps({"ok": True, "order": order})

# TODO 3: Create model and model_with_tools = model.bind_tools(...)
model = ChatOllama(model="qwen2.5-coder:7b", base_url="localhost:11434", temperature=0, num_predict=512, disable_streaming=False,verbose=True)
model_with_tools = model.bind_tools([get_order_status])
parser = StrOutputParser()
def run_order_help(user_query: str):
  # TODO 4: Build messages, invoke, handle tool_calls or return early,
  #         then second invoke after ToolMessage(s)
  messages = [(SystemMessage(content="use the order tool when the user asks about an order and give a helpful response")), (HumanMessage(content=user_query))]
  response = model_with_tools.invoke(messages)
  messages.append(response)
  print(response.content)

  print("Tool calls:", response.tool_calls)

  for tool_call in response.tool_calls:
    tool_response = tool_call.invoke(tool_call["args"])
    messages.append(ToolMessage(content = str(tool_response), tool_call_id = tool_call["id"]))
    response = model_with_tools.invoke(messages)
    final_resonse  = model_with_tools.invoke(messages)
    return final_resonse.content



if __name__ == "__main__":
    # TODO 5: Run the two test queries and print answers
    print(run_order_help("What is the status of order CC2001?"))