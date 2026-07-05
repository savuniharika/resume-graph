import streamlit as st
from graphs.resume_graph import graph # Replace with your actual filename

st.set_page_config(
    page_title="AI Resume Interviewer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Interviewer")
st.write("Analyze a resume, generate interview questions, and evaluate answers.")

# ------------------------
# Resume Input
# ------------------------

resume = st.text_area(
    "Paste Resume",
    height=250,
    placeholder="Paste the candidate's resume here..."
)

# ------------------------
# Candidate Answer
# ------------------------

answer = st.text_area(
    "Candidate Answer",
    height=150,
    placeholder="Enter the candidate's answer..."
)

# ------------------------
# Button
# ------------------------

if st.button("Start Interview"):

    if resume.strip() == "":
        st.warning("Please paste a resume.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        result = graph.invoke({
            "resume": resume,
            "answer": answer
        })

    st.success("Completed Successfully!")

    st.divider()

    st.subheader("📄 Resume Analysis")
    st.write(result["analysis"])

    st.divider()

    st.subheader("❓ Interview Questions")
    st.write(result["questions"])

    st.divider()

    st.subheader("📊 Answer Evaluation")
    st.write(result["evaluation"])