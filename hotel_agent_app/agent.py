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
    instruction="Today date is {date}, Use the provided `operation_tools` to perform tasks related to hotel operations.",
    tools=operation_tools
)

hotel_operation_tools = AgentTool(agent=hotel_operation_agent)

analytics_tools = toolbox.load_toolset('hotel_analytics')

hotel_analytics_agent = Agent(
    model= model,
    name='hotel_analytics_agent',
    description="Agent to assist with hotel business analytics tasks.",
    instruction="Today date is {date}, Use the provided `analytics_tools` to perform tasks related to hotel business analytics.",
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