from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from ...tools import toolbox, model

operation_tools = toolbox.load_toolset('hotel_operations')

hotel_operation_agent = LlmAgent(
    model= model,
    name='hotel_operations_agent',
    description="Agent to assist with hotel operations tasks.",
    instruction="""    
    1. ALWAYS use the parameter {current_date} as the reference for today's date when interpreting queries. This is mandatory for all time-relative queries (e.g., 'today', 'yesterday', 'tomorrow', 'next week', 'next month').
    2. Use the provided `operation_tools` to perform tasks related to hotel operations."
    3. IMPORTANT: After receiving data from a tool, you MUST synthesize it into a clear, human-readable summary. "
    4. Do not output raw data or JSON. "
    5. For Example: We have 4 'Deluxe King' rooms available from 2025-06-23 to 2025-06-24. Room numbers are 101 and 102, both with a daily rate of $220.50."
    """,
    tools=operation_tools,
    output_key="operation_summary",
)

hotel_operation_tools = AgentTool(agent=hotel_operation_agent)