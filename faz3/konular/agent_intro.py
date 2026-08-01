# faz3/konular/agent_intro.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from google import genai

# Gemini elçimizi başlatıyoruz.
client = genai.Client()
