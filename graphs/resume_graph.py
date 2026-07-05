import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Define the state
class ResumeState(TypedDict):
    resume: str
    analysis: str
    questions:str
    answer:str
    evaluation:str

# Analyze resume
def analyze_resume(state: ResumeState):
    print("Analyzing resume...")

    prompt = f"""
    Analyze this resume:
    {state["resume"]}
    """

    response = model.generate_content(prompt)

    return {"analysis": response.text}


# generate questions
def generate_questions(state: ResumeState):
    print("Generating interview questions...")

    prompt = f"""
    Based on the candidate profile below:

    {state["analysis"]}

    Generate exactly 5 interview questions.

    For each question provide:

    Question:
    Ideal Answer:
    Difficulty (Easy/Medium/Hard)

    Format:

    Question 1:
    ...

    Ideal Answer:
    ...

    Difficulty:
    ...

    Repeat the same format for all 5 questions.
    """

    response = model.generate_content(prompt)

    state["questions"] = response.text

    return state


# evaluate answers
def evaluate_answer(state: ResumeState):
    print("Evaluating answer...")

    prompt = f"""
    You are an AI interviewer.

    These are the interview questions and their ideal answers:

    {state["questions"]}

    Candidate's answer:

    {state["answer"]}

    Compare the candidate's answer with the ideal answer.

    Provide:

    Score: /10

    Strengths:
    - ...

    Weaknesses:
    - ...

    Suggestions:
    - ...
    """

    response = model.generate_content(prompt)

    state["evaluation"] = response.text

    return state


# -------------------------
# Create the graph
# -------------------------
# -------------------------
# Create the graph
# -------------------------

builder = StateGraph(ResumeState)

# Add nodes
builder.add_node("analyze_resume", analyze_resume)
builder.add_node("generate_questions", generate_questions)
builder.add_node("evaluate_answer",evaluate_answer)

# Connect flow
builder.add_edge(START, "analyze_resume")
builder.add_edge("analyze_resume", "generate_questions")
builder.add_edge("generate_questions", "evaluate_answer")
builder.add_edge("evaluate_answer",END)

# Compile graph
graph = builder.compile()
# Run graph
result = graph.invoke({
    "resume": "I am an EEE student interested in AI and Python.",
    "answer":"i know python basics and i have done a small AI project using sklearn."
})

print("\n===== ANALYSIS =====\n")
print(result["analysis"])

print("\n===== QUESTIONS =====\n")
print(result["questions"])

print("\n====EVALUATION====\n")
print(result["evaluation"])