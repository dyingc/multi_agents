from langchain_core.messages import HumanMessage,AIMessage

def parse_langgraph_output(stream):
    results = []
    for key, value in stream.items():
        if key == "supervisor":
            continue
        messages = value.get("messages", [])
        for msg in messages:
            if isinstance(msg, str):
                results.append((key, msg))
            elif isinstance(msg, AIMessage):
                results.append((key, msg.content))
    return results

import logging
import os

# Create logs directory if it doesn't exist
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)

# Define log file path
log_file = os.path.join(log_directory, "wellness_app.log")

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # You can change this to INFO or ERROR as needed
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='a'),
        logging.StreamHandler()  # Optional: Also logs to console
    ]
)

# Example usage
app_logger = logging.getLogger("WellnessApp")
app_logger.setLevel(logging.INFO)
app_logger.info("Logger is set up and ready to use.")