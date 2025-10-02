import logging
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.hotel_operation.agent import hotel_operation_tools
from .sub_agents.hotel_analytics.agent import hotel_analytics_tools
from .sub_agents.data_visualization.agent import visualization_tool
from .tools import model

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

root_agent = Agent(
    name="hotel_agent",
    model=model,
    description=(
        "Agent to help hotel staff by answering questions and performing tasks related to hotel operations and business analytics."
    ),
    instruction=(
        "1. Use `hotel_operation_tools` for hotel operations tasks."
        "2. Use `hotel_analytics_tools` for business analytics tasks."
        "3. Use `visualization_tool` to create charts and graphs based on data."
    ),
    tools=[
        hotel_operation_tools,
        hotel_analytics_tools,
        visualization_tool
    ]
)