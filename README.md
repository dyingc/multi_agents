[Reference](https://levelup.gitconnected.com/how-to-build-a-multi-agent-supervisor-system-with-langgraph-qwen-streamlit-2aabed617468)

# Multi-Agent Supervisor System with LangGraph, Qwen, and Streamlit
This project demonstrates how to build a multi-agent supervisor system using LangGraph, Qwen, and Streamlit. The system is designed to manage multiple agents that can perform tasks based on user input.

# The Supervisor Architecture
![Supervisor Architecture](./imgs/supervisor_architecture.png)

# Step 1: Installation
Before we can use Qwen locally, we need to install Ollama, which allows us to run large language models directly on our machine.

i)Download and Install Ollama

To download Ollama, go to their [official website](https://ollama.com/download/linux) and download the version compatible with your operating system.

ii) Verify Installation

```bash
ollama -v
```

ii) Pull the Qwen Model

```bash
ollama pull qwen2.5:14b
```

# Step 2: Set Up API Keys
Our system will rely on external APIs to provide real-world data for the Fitness Agent and the Dietitian Agent. These agents will fetch exercise and nutrition information from these respective APIs.

## APIs Used:

- Fitness Agent : [API-Ninjas Exercise API](https://api-ninjas.com/api/exercises)
- Dietitian Agent : [Spoonacular Food & Nutrition API](https://spoonacular.com/food-api/console#Profile)

i) Get Your API Keys

Sign up for free accounts on both platforms and retrieve your API keys.

ii) Store Keys

To keep our credentials secure and easily accessible, we’ll store them in a .env file.

The .env file will look like this;

```
EXERCISE_API_KEY=xxxxxxxx 
DIET_API_KEY=xxxxxxxxxxxx
```

