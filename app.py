import streamlit as st
import asyncio
from hotel_agent_app.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.artifacts import GcsArtifactService
from google.genai import types as genai_types
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# --- Environment Configuration ---
# Ensure these environment variables are set in your .env file or system
os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = os.getenv("GOOGLE_GENAI_USE_VERTEXAI")

# PostgreSQL Database Connection Details
# POSTGRES_HOST = os.getenv("POSTGRES_LOCALHOST")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_SESSIONDB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_current_date() -> str:
    """Get the current date in WIB timezone and return it as a formatted string."""
    wib_timezone = datetime.timezone(datetime.timedelta(hours=7))
    now = datetime.datetime.now(wib_timezone)
    return now.strftime('%Y-%m-%d')

# --- Page Configuration ---
st.set_page_config(
    page_title="Hotel Management Assistant",
    page_icon="🏨",
    layout="centered"
)

# --- Custom CSS for a Hotel Theme ---
st.markdown("""
<style>
    /* --- Professional Hotel Theme (Blue & White) --- */
    :root {
        --bg-color: #f8f9fa; /* Light Gray */
        --text-color: #2F4F4F; /* Dark Slate Gray */
        --title-color: #17a2b8; /* Professional Teal */
        --caption-color: #6c757d; /* Muted Gray */
        --chat-bg: #ffffff;
        --chat-border: #ced4da;
        --button-bg: #ffffff;
        --button-text: #17a2b8;
        --button-border: #17a2b8;
        --button-hover-bg: #17a2b8; /* Solid teal on hover */
        --button-hover-text: #ffffff; /* White text on hover */
    }
    
    .stApp { background-color: var(--bg-color); }
    h1 { color: var(--title-color); }
    .stMarkdown, div[data-testid="stMarkdownContainer"] p { color: var(--text-color); }
    [data-testid="stCaption"] { color: var(--caption-color); }
    
    /* Styling for chat bubbles */
    .st-emotion-cache-1c7y2kd {
        background-color: var(--chat-bg);
        border: 1px solid var(--chat-border);
    }
    .st-emotion-cache-1c7y2kd .stMarkdown { color: var(--text-color); }

    .stButton>button {
        font-size: 0.9rem;
        background-color: var(--button-bg);
        color: var(--button-text);
        border: 1px solid var(--button-border);
        border-radius: 5px;
        font-weight: 500;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: var(--button-hover-bg);
        color: var(--button-hover-text);
        border: 1px solid var(--button-border); /* Keep original border on hover */
    }

    /* Dark Mode Option (activated by system preference) */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: #0a192f; /* Very Dark Blue */
            --text-color: #ccd6f6; /* Light Slate */
            --title-color: #58a6ff; /* Bright Blue for dark mode */
            --caption-color: #8892b0; /* Slate */
            --chat-bg: #112240; /* Lighter Dark Blue */
            --chat-border: #233554;
            --button-bg: #112240;
            --button-text: #58a6ff;
            --button-border: #58a6ff;
            --button-hover-bg: rgba(88, 166, 255, 0.2); /* Slightly more visible hover */
            --button-hover-text: #58a6ff;
        }
    }
</style>
""", unsafe_allow_html=True)


# --- Setup Runner and Session Service (cached to prevent recreation) ---
@st.cache_resource
def setup_adk_runner():
    session_service = DatabaseSessionService(db_url=DATABASE_URL)
    artifact_service = GcsArtifactService(bucket_name=os.getenv("GCS_BUCKET_NAME"))
    runner = Runner(
        agent=root_agent,
        app_name="hotel_management_app",
        session_service=session_service,
        artifact_service=artifact_service
    )
    return runner, session_service

runner, session_service = setup_adk_runner()
USER_ID = "hotel_user"

# --- Use Streamlit's session state to manage a unique session ID ---
if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit_session_{datetime.datetime.now().timestamp()}"
SESSION_ID = st.session_state.session_id


# --- Initialize ADK Session (only once per app start) ---
if "session_initialized" not in st.session_state:
    try:
        asyncio.run(session_service.create_session(
            app_name=runner.app_name,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state={
                "current_date": get_current_date(),
                "analytics_summary": "",  
                "operation_summary": ""   
                }
        ))
        st.session_state.session_initialized = True
        st.session_state.messages = [{"role": "assistant", "content": "Welcome to the Hotel Management Assistant! How can I help you?"}]
    except Exception as e:
        st.error(f"Failed to initialize the conversation session: {e}")
        st.stop()

# --- NEW: Combined async function to get response and artifacts ---
async def get_agent_response_and_artifacts_async(prompt, runner, user_id, session_id):
    """Runs the ADK agent and also fetches any generated image artifacts."""
    content = genai_types.Content(role='user', parts=[genai_types.Part(text=prompt)])
    final_response_text = "Sorry, an error occurred while processing your request."
    final_image_data = None

    # 1. Run the agent to get the text response
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            break
    
    # 2. After the agent run, check for artifacts
    try:
        artifact_keys = await runner.artifact_service.list_artifact_keys(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
        )
        image_keys = [key for key in artifact_keys if key.startswith('code_execution_image_') and key.endswith('.png')]

        if image_keys:
            # Load the most recent image artifact
            key = image_keys[-1]
            loaded_artifact = await runner.artifact_service.load_artifact(
                app_name=runner.app_name,
                user_id=user_id,
                session_id=session_id,
                filename=key
            )
            if loaded_artifact:
                final_image_data = loaded_artifact.inline_data.data
                # Clean up by deleting the artifact
                await runner.artifact_service.delete_artifact(
                    app_name=runner.app_name,
                    user_id=user_id,
                    session_id=session_id,
                    filename=key
                )
    except Exception as e:
        # Log for debugging, but don't show an error to the user
        st.error(f"Artifact discovery/loading failed: {e}",icon="🚨")

    return {"text": final_response_text, "image_data": final_image_data}


# --- Main Title ---
st.title("🏨 Hotel Management Assistant")
st.markdown("Ask about room availability, bookings, or business analytics.")

# --- Display existing Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # NEW: Check if the message object has image data and display it
        if message.get("image_data"):
            st.image(message["image_data"], use_container_width=True)

# --- Logic to process new input ---
prompt_to_process = None

# Display example question buttons
st.markdown("---")
st.caption("Or, start with one of these questions:")
col1, col2 = st.columns(2)
example_questions = [
    "Find available Standard Queen rooms for 1 night during this coming weekend",
    "What was the total revenue for each month this year?",
    "What were the top booking channels this year?",
    "Create a new booking for guest 2 in room 1 for next wednesday, for 1 night."
]
if col1.button(example_questions[0], use_container_width=True):
    prompt_to_process = example_questions[0]
if col2.button(example_questions[1], use_container_width=True):
    prompt_to_process = example_questions[1]
if col1.button(example_questions[2], use_container_width=True):
    prompt_to_process = example_questions[2]
if col2.button(example_questions[3], use_container_width=True):
    prompt_to_process = example_questions[3]

if chat_input_prompt := st.chat_input("Ask about rooms, bookings, or analytics..."):
    prompt_to_process = chat_input_prompt

# --- UPDATED: Main processing block ---
if prompt_to_process:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})

    # Show spinner while getting the complete agent response (text + image)
    with st.spinner("The assistant is thinking..."):
        response_data = asyncio.run(get_agent_response_and_artifacts_async(
            prompt=prompt_to_process,
            runner=runner,
            user_id=USER_ID,
            session_id=SESSION_ID
        ))

    # Create a single assistant message with both text and image data
    assistant_message = {
        "role": "assistant",
        "content": response_data["text"],
        "image_data": response_data["image_data"]
    }
    st.session_state.messages.append(assistant_message)

    # Rerun the app to display the latest messages
    st.rerun()