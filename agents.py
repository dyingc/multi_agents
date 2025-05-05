from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain.prompts import PromptTemplate
from typing import Annotated
from typing_extensions import TypedDict
from enum import Enum

from langchain_ollama import ChatOllama

from langgraph.types import Command
from utils import app_logger
from tools import fitness_data_tool, diet_tool
import streamlit as st

# ---------------- Configuration ----------------

llm = ChatOllama(
    model="qwen3:30b", # "qwen3:14b",
    base_url="http://localhost:8450", # Using ssh forward channel redirected to: HyperML "http://127.0.0.1:8450",
    temperature=0.0
)

memory = MemorySaver()

# Define Enum for safe routing
class Node(str, Enum):
    fitness = "fitness"
    dietitian = "dietitian"
    wellness = "wellness"
    end = "__end__"

members = [Node.fitness, Node.dietitian, Node.wellness]
options = members + [Node.end]

fitness_agent_prompt = "You can only answer queries related to workout."
dietitian_system_prompt = "You can only answer queries related to diet and meal plans."

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {', '.join([m.value for m in members])}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH.\n"
    "Guidelines:\n"
    "1. Always check the last message in the conversation to determine if the task has been completed.\n"
    "2. If you already have the final answer or outcome, return 'FINISH'.\n"
)

# ---------------- Agents ----------------

fitness_agent = create_react_agent(llm, tools=[fitness_data_tool], prompt=fitness_agent_prompt)
dietitian_agent = create_react_agent(llm, tools=[diet_tool], prompt=dietitian_system_prompt)

# ---------------- State ----------------

class State(MessagesState):
    next: Node

class Router(TypedDict):
    next: Node

# ---------------- Nodes ----------------

def fitness_node(state: State) -> Command[Node]:
    result = fitness_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="fitness")
            ]
        },
        goto="supervisor",
    )

def dietitian_node(state: State) -> Command[Node]:
    result = dietitian_agent.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=result["messages"][-1].content, name="dietitian")
            ]
        },
        goto="supervisor",
    )

def mental_health_node(state: State) -> Command[Node]:
    prompt = PromptTemplate.from_template(
        """You are a supportive mental wellness coach.
        Your task is to:
        - Give a unique mental wellness tip or stress-reducing practice.
        - Make it simple, kind, and useful. Avoid repeating tips."""
    )
    chain = prompt | llm
    response = chain.invoke(state)
    return Command(
        update={
            "messages": [
                AIMessage(content=f"Here's your wellness tip: {response.content}", name="wellness")
            ]
        },
        goto="supervisor",
    )

def supervisor_node(state: State) -> Command[Node]:
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    app_logger.info(f"Router response: {response}")
    goto = response["next"]
    if goto == "FINISH":
        goto = Node.end
    return Command(goto=goto, update={"next": goto})