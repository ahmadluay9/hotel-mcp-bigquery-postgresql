from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from ...tools import toolbox, model

analytics_tools = toolbox.load_toolset('hotel_analytics')

hotel_analytics_agent = LlmAgent(
    model= model,
    name='hotel_analytics_agent',
    description="Agent to assist with hotel business analytics tasks.",
    instruction="""    
    1. Always use the parameter {current_date} as the reference for today's date when interpreting queries. This is mandatory for all time-relative queries (e.g., 'today', 'yesterday', 'tomorrow', 'next week', 'next month', 'this year').
    2. Use the provided `analytics_tools` to perform tasks related to hotel business analytics.
    3. IMPORTANT: After receiving data from a tool, you MUST synthesize it into a clear, human-readable summary. 
    4. Do not output raw data or JSON.  
    5. Ask if the user wants a data visualization of the analytics data.
    6. Example: 'The total revenue for each month in 2023 is as follows: 
    - January: $2011.50 
    - February: $1981.50 
    - March: $1563.00
    - April: $1745.00'
    """,
    tools=analytics_tools,
    output_key="analytics_summary",
)

hotel_analytics_tools = AgentTool(agent=hotel_analytics_agent)