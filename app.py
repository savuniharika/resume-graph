import streamlit as st
from graphs.resume_graph import (
    analyze_resume,
    generate_questions,
    evaluate_answer,
)

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Interview Assistant")

resume = st.text_area(
    "Paste Resume",
    height=250
)

if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

# ----------------------------
# Step 1
# ----------------------------

if st.button("Generate Interview Questions"):

    analysis = analyze_resume(resume)

    questions = generate_questions(analysis)

    st.session_state.analysis = analysis
    st.session_state.questions = questions

# ----------------------------
# Show Results
# ----------------------------

if st.session_state.analysis:

    st.subheader("Resume Analysis")

    st.write(st.session_state.analysis)

    st.subheader("Interview Questions")

    for i, q in enumerate(st.session_state.questions, 1):
        st.write(f"**{i}. {q}**")

# ----------------------------
# Step 2
# ----------------------------

if st.session_state.questions:

    answer = st.text_area(
        "Write your answers here",
        height=250
    )

    if st.button("Evaluate Answer"):

        evaluation = evaluate_answer(
            st.session_state.analysis,
            st.session_state.questions,
            answer
        )

        st.subheader("Evaluation")

        st.write(evaluation)