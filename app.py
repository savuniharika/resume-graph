from graphs.resume_graph import graph

resume_text = """
Software engineer skilled in Python, FastAPI, Machine Learning, and SQL.
Built chatbot using Gemini API and deployed on cloud.
"""

result = graph.invoke({
    "resume": resume_text,
    "answer": "I built an AI chatbot using FastAPI and Gemini API for smart responses."
})

print("\n--- ANALYSIS ---\n")
print(result["analysis"])

print("\n--- QUESTIONS ---\n")
print(result["questions"])

print("\n--- EVALUATION ---\n")
print(result["evaluation"])