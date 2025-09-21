# Hotel Management AI Assistant
This project is a sophisticated AI-powered chatbot designed to act as a Hotel Management Assistant. It provides a conversational interface for both operational tasks (like checking room availability) and analytical queries (like reviewing monthly revenue).

The application is built using **Streamlit** for the user interface, Google's **Agent Development Kit (ADK)** for the core agent logic, and connects to a dual-database backend: **PostgreSQL** for real-time transactional data and **Google BigQuery** for business intelligence and analytics.

## Features
- **Conversational Interface**: An intuitive chat application built with Streamlit.

- **Operational Capabilities**:

    - Find available rooms based on dates and room types.

    - Create new guest bookings.

- **Analytical Capabilities**:

    - Calculate and report total monthly revenue for a given year.

    - Analyze the top-performing booking channels over a specific period.

- **Persistent Chat Sessions**: Uses a PostgreSQL database to store and manage user chat sessions, allowing for stateful conversations.

- **Containerized & Deployable**: Includes a Dockerfile and cloudbuild.yaml for easy containerization and deployment to Google Cloud.

## Project Structure
```
hotel-mcp-bigquery-postgresql/
├── hotel_agent_app/
│   └── agent.py         # Core ADK agent definition and instructions.
├── mcp-toolbox/
│   └── tools.yaml       # Defines agent's skills (tools) via MCP.
├── .env                 # Local environment variables (credentials, configs).
├── README.md            # This project overview file.
├── .gitignore           # Specifies files for Git to ignore.
├── cloudbuild.yaml      # Configuration for Google Cloud Build.
├── Dockerfile           # Instructions to build the application container image.
├── app.py               # The main Streamlit frontend application.
├── notebook.ipynb       # Jupyter notebook for testing and experimentation.
└── requirements.txt     # List of Python dependencies.
```

## Architecture
The application uses a modern, decoupled architecture:

- **Frontend**: A Python-based web interface created with **Streamlit** (`app.py`).

- **Agent Logic**: The core conversational agent is defined in `hotel_agent_app/agent.py` using the **Google Agent Development Kit (ADK)**.

- **Tooling Layer**: The agent's capabilities (tools) are defined using the **Model Context Protocol (MCP)**, allowing it to execute SQL queries against the databases.

- **Databases**:

    - **PostgreSQL**: Serves as the OLTP (Online Transaction Processing) database for operational data like room status and bookings. It also stores the chat session history.

    - **Google BigQuery**: Serves as the OLAP (Online Analytical Processing) data warehouse for running fast, complex analytical queries.

- **Session Management**: The `DatabaseSessionService` from the ADK is used to persist chat history in the PostgreSQL database.

## Reference

[1. Deploy MCP to Cloud Run](https://googleapis.github.io/genai-toolbox/how-to/deploy_toolbox/)

[2. Quickstart (MCP with BigQuery)](https://googleapis.github.io/genai-toolbox/samples/bigquery/mcp_quickstart/)

[3. Build a Travel Agent using MCP Toolbox for Databases and Agent Development Kit (ADK)](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk?hl=en)
