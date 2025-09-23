from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from toolbox_core import ToolboxSyncClient
import os
from dotenv import load_dotenv
load_dotenv()

model=os.getenv("MODEL")

toolbox = ToolboxSyncClient(os.getenv("CLOUD_RUN_SERVICE_URL"))
# toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

operation_tools = toolbox.load_toolset('hotel_operations')

hotel_operation_agent = Agent(
    model= model,
    name='hotel_operations_agent',
    description="Agent to assist with hotel operations tasks.",
    instruction=(
    "If a user's query is relative to the current time (e.g., 'today', 'tomorrow', 'next month'), "
    "you MUST use the {date} first to establish the context."
    "Use the provided `operation_tools` to perform tasks related to hotel operations."
    "IMPORTANT: After receiving data from a tool, you MUST synthesize it into a clear, human-readable summary. "
    "Do not output raw data or JSON. "
    "For Example: We have 4 'Deluxe King' rooms available from 2025-06-23 to 2025-06-24. Room numbers are 101 and 102, both with a daily rate of $220.50."
    ),
    tools=operation_tools
)

hotel_operation_tools = AgentTool(agent=hotel_operation_agent)

analytics_tools = toolbox.load_toolset('hotel_analytics')

hotel_analytics_agent = Agent(
    model= model,
    name='hotel_analytics_agent',
    description="Agent to assist with hotel business analytics tasks.",
    instruction="""
    1. If a user's query is relative to the current time (e.g., 'today', 'tomorrow', 'next month'), 
    you MUST use the {date} first to establish the context.    
    2. Use the provided `analytics_tools` to perform tasks related to hotel business analytics.
    3. IMPORTANT: After receiving data from a tool, you MUST synthesize it into a clear, human-readable summary. 
    4. Do not output raw data or JSON.  
    5. Example: 'The total revenue for each month in 2023 is as follows: 
    - January: $2011.50 
    - February: $1981.50 
    - March: $1563.00
    - April: $1745.00'
    """,
    tools=analytics_tools
)

hotel_analytics_tools = AgentTool(agent=hotel_analytics_agent)

root_agent = Agent(
    name="hotel_agent",
    model=model,
    description=(
        "Agent to help hotel staff by answering questions and performing tasks related to hotel operations and business analytics."
    ),
    instruction=(
        "Use `hotel_operation_tools` for hotel operations tasks."
        "Use `hotel_analytics_tools` for business analytics tasks."        
    ),
    tools=[
        hotel_operation_tools,
        hotel_analytics_tools,
    ]
)