from toolbox_core import ToolboxSyncClient
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize model clients
model=os.getenv("MODEL")

# Initialize Toolbox client
# toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
toolbox = ToolboxSyncClient(os.getenv("CLOUD_RUN_SERVICE_URL"))