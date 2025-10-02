# Hotel Management AI Assistant
![hotel-mcp-bq](https://github.com/user-attachments/assets/3fee4eb6-9e70-40e1-b300-daab429e762f)
This project is a sophisticated AI-powered chatbot designed to act as a Hotel Management Assistant. It provides a conversational interface for both operational tasks (like checking room availability) and analytical queries (like reviewing monthly revenue).


The application is built using **Streamlit** for the user interface, Google's **Agent Development Kit (ADK)** for the core agent logic, and connects to a dual-database backend: **PostgreSQL** for real-time transactional data and **Google BigQuery** for business intelligence and analytics.

## Features
- **Conversational Interface**: An intuitive chat application built with Streamlit.

- **Hierarchical Agent System**: A multi-agent architecture where a root agent delegates tasks to specialized agents for operations, analytics, and data visualization.

- **Operational Capabilities**:

    - Find available rooms based on dates and room types.

    - Create new guest bookings.

- **Analytical Capabilities**:

    - Calculate and report total monthly revenue for a given year.

    - Analyze the top-performing booking channels over a specific period.

- **Dynamic Chart Generation**: Automatically generates and displays charts (e.g., bar charts for revenue) using a dedicated visualization agent.

- **Persistent Sessions & Artifacts**: 

    - Uses a **PostgreSQL** database to store and manage user chat sessions, allowing for stateful conversations.

    - Leverages **Google Cloud Storage (GCS)** via the `GcsArtifactService` to handle file artifacts (like generated charts) in a scalable, production-ready manner.

- **Containerized & Deployable**: Includes a Dockerfile and `cloudbuild.yaml` for easy containerization and deployment to Google Cloud.

## Project Structure
This repository is organized to separate concerns, making it modular and scalable. Each file and directory has a distinct role:

```
hotel-mcp-bigquery-postgresql/
├── hotel_agent_app/
│   ├── sub_agents
│   │   ├── data_visualization
│   │   │   ├──__init__.py
│   │   │   └──agent.py
│   │   ├── hotel_analytics
│   │   │   ├──__init__.py
│   │   │   └──agent.py
│   │   └── hotel_operation
│   │       ├──__init__.py
│   │       └──agent.py             
│   ├──__init__.py      
│   ├── agent.py        
│   └── tools.py         
├── mcp-toolbox/
│   └── tools.yaml
├── README.md            
├── .gitignore           
├── cloudbuild.yaml      
├── Dockerfile           
├── app.py               
├── notebook.ipynb       
└── requirements.txt
```

- `hotel_agent_app/`: The main Python package for the AI agent.

    - `sub_agents/`: Contains the specialized "worker" agents for specific tasks.

    - `agent.py`: Defines the main "root" agent which acts as a router, delegating tasks to the appropriate sub-agent.

    - `tools.py`: A utility script that initializes and configures the MCP Toolbox client.

- `mcp-toolbox/tools.yaml`: Defines the agent's database skills. It uses the Model Context Protocol (MCP) to map natural language descriptions to specific SQL queries.

- `app.py`: The user-facing frontend built with Streamlit. It creates the chat UI, manages the conversation flow, and handles the display of text and image artifacts returned by the agent.

- `Dockerfile` & `cloudbuild.yaml`: Files for DevOps. Dockerfile packages the application into a container, and cloudbuild.yaml automates the build/deployment process on Google Cloud.

- `requirements.txt`: Lists all Python libraries the project depends on.

- `notebook.ipynb`: A Jupyter Notebook for interactive development and testing.

## Architecture
### System Architecture
<img width="3808" height="2056" alt="image" src="https://github.com/user-attachments/assets/f680074a-43db-4ab3-9857-8e3b07eae71a" />

### AI Agentic Workflow
<img width="943" height="868" alt="image" src="https://github.com/user-attachments/assets/51454b1f-0f12-4a7a-830a-e431036e3810" />

### MCP Server - Database Toolbox
<img width="2684" height="1968" alt="image" src="https://github.com/user-attachments/assets/c9846cd5-4411-4799-acbc-26c3f2238edf" />

The application uses a modern, decoupled architecture:

1. **Data Sources**: PostgreSQL (`hotel_db`) is the OLTP database for live operational data, while BigQuery (`hotel_dataset`) is the OLAP data warehouse for analytics.

2. **Tooling Ecosystem**: The MCP Server (on Cloud Run) acts as a secure API gateway to the databases.

3. **Orchestration Layer**: The Hotel Agent (on Cloud Run) manages the conversation, deciding which tool or sub-agent to use.

4. Session & Artifact Management:

    - A PostgreSQL database (`hotel_session_db`) stores conversation history.

    - Google Cloud Storage is used by the `GcsArtifactService` to manage file artifacts (like charts) generated during code execution.

5. DevOps & AI: The system is automated via a CI/CD pipeline (Cloud Build), with containers in Artifact Registry. The core intelligence is a Gemini model on Vertex AI.

## Reference

[1. Deploy MCP to Cloud Run](https://googleapis.github.io/genai-toolbox/how-to/deploy_toolbox/)

[2. Quickstart (MCP with BigQuery)](https://googleapis.github.io/genai-toolbox/samples/bigquery/mcp_quickstart/)

[3. Build a Travel Agent using MCP Toolbox for Databases and Agent Development Kit (ADK)](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk?hl=en)
