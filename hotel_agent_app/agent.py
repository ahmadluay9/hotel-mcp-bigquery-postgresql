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
    instruction="""    
    1. Use the provided `operation_tools` to perform tasks related to hotel operations."
    2. IMPORTANT: After receiving data from a tool, you MUST synthesize it into a clear, human-readable summary. "
    3. Do not output raw data or JSON. "
    4. For Example: We have 4 'Deluxe King' rooms available from 2025-06-23 to 2025-06-24. Room numbers are 101 and 102, both with a daily rate of $220.50."
    """,
    tools=operation_tools
)

hotel_operation_tools = AgentTool(agent=hotel_operation_agent)

analytics_tools = toolbox.load_toolset('hotel_analytics')

hotel_analytics_agent = Agent(
    model= model,
    name='hotel_analytics_agent',
    description="Agent to assist with hotel business analytics tasks.",
    instruction="""    
    1. Use the provided `analytics_tools` to perform tasks related to hotel business analytics.
    2. IMPORTANT: After receiving data from a tool, you MUST synthesize it into a clear, human-readable summary. 
    3. Do not output raw data or JSON.  
    4. Example: 'The total revenue for each month in 2023 is as follows: 
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
        "1. ALWAYS use the parameter {current_date} as the reference for today's date when interpreting queries. "
        "This is mandatory for all time-relative queries (e.g., 'today', 'yesterday', 'tomorrow', 'next week', 'next month'). "
        "2. Use `hotel_operation_tools` for hotel operations tasks."
        "3. Use `hotel_analytics_tools` for business analytics tasks."
    ),
    tools=[
        hotel_operation_tools,
        hotel_analytics_tools,
    ]
)