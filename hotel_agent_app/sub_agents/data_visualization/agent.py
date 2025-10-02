from google.adk.agents import LlmAgent
from google.adk.code_executors import VertexAiCodeExecutor
from google.adk.tools.agent_tool import AgentTool
from ...tools import toolbox, model

data_visualization_agent = LlmAgent(
    model=model,
    name='data_visualization_agent',
    description="Agent that creates data visualizations like charts and graphs based on provided data.",
    instruction="""
    You are a data visualization specialist. Your primary function is to create charts and graphs using Python.
    1. Use {analytics_summary} as the data source.
    2. Your task is to write Python code to visualize this data.
    3. Use libraries like `matplotlib` and `seaborn` for plotting.
    4. **Crucially, you must wrap your Python code in ```python ... ``` blocks.** The code executor will run this code.
    6. After generating the code to create the visualization, provide a brief, one-sentence summary of what the visualization shows.
    """,
    # The code_executor enables this agent to run code.
    code_executor=VertexAiCodeExecutor(
        optimize_data_file=True,
        stateful=True,
    ),
)

visualization_tool = AgentTool(agent=data_visualization_agent)