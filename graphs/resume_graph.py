import os
from typing import TypedDict, List
import google.generativeai as genai

from langgraph.graph import StateGraph, START, END

# -------------------------
# Gemini Setup
# -------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


# -------------------------
# State
# -------------------------
class ResumeState(TypedDict):
    resume: str
    analysis: str
    questions: List[str]
    answer: str
    evaluation: str


# -------------------------
# Node 1: Analyze Resume
# -------------------------
def analyze_resume(state: ResumeState):
    prompt = f"""
    Analyze the resume and extract:
    - Skills
    - Strengths
    - Weaknesses

    Resume:
    {state['resume']}
    """

    response = model.generate_content(prompt)

    return {"analysis": response.text}


# -------------------------
# Node 2: Generate Questions
# -------------------------
def generate_questions(state: ResumeState):
    prompt = f"""
    Based on this resume analysis, generate 5 technical interview questions.

    Analysis:
    {state['analysis']}

    Return as a numbered list.
    """

    response = model.generate_content(prompt)

    questions = response.text.split("\n")

    return {"questions": questions}


# -------------------------
# Node 3: Evaluate Answer
# -------------------------
def evaluate_answer(state: ResumeState):
    prompt = f"""
    You are an interviewer.

    Resume Analysis:
    {state['analysis']}

    Questions:
    {state['questions']}

    Candidate Answer:
    {state['answer']}

    Give:
    - Score out of 10
    - Feedback
    """

    response = model.generate_content(prompt)

    return {"evaluation": response.text}


# -------------------------
# Build Graph
# -------------------------
builder = StateGraph(ResumeState)

# Add nodes
builder.add_node("analyze_resume", analyze_resume)
builder.add_node("generate_questions", generate_questions)
builder.add_node("evaluate_answer", evaluate_answer)

# Add edges (FLOW)
builder.add_edge(START, "analyze_resume")
builder.add_edge("analyze_resume", "generate_questions")
builder.add_edge("generate_questions", "evaluate_answer")
builder.add_edge("evaluate_answer", END)

# Compile graph
graph = builder.compile()