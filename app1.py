import streamlit as st
import PyPDF2
import os
import google.generativeai as genai

# Configure Gemini API using Streamlit secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# --------- UTILITY FUNCTIONS ----------

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def summarize_document(text):
    response = model.generate_content(
        f"Summarize the following document in no more than 150 words:\n\n{text}"
    )
    return response.text.strip()

def answer_question(document, question):
    prompt = (
        f"Document:\n{document}\n\n"
        f"Answer the question below using only information from the document. "
        "Provide a brief justification and mention the section/paragraph:\n\n"
        f"Question: {question}\nAnswer:"
    )
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_logic_questions(document):
    prompt = (
        f"Document:\n{document}\n\n"
        "Generate three logic-based or comprehension-focused questions from the document.\n"
        "List them as Q1, Q2, Q3."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

def evaluate_answer(document, question, user_answer):
    prompt = (
        f"Document:\n{document}\n\n"
        f"Question: {question}\n"
        f"User's Answer: {user_answer}\n\n"
        "Evaluate the answer. Provide feedback and justify with a reference from the document."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

def highlight_snippet(document, answer):
    prompt = (
        f"Document:\n{document}\n\n"
        f"Answer: {answer}\n\n"
        "Find the most relevant snippet from the document that supports this answer. Return only the snippet."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

# --------- STREAMLIT INTERFACE ----------

st.set_page_config(page_title="📄 Smart Research Assistant", layout="wide")
st.title("📄 Smart Research Assistant with Gemini")

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "questions" not in st.session_state:
    st.session_state.questions = []
if "mode" not in st.session_state:
    st.session_state.mode = None

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    # Read document
    if uploaded_file.type == "application/pdf":
        doc_text = extract_text_from_pdf(uploaded_file)
    else:
        doc_text = uploaded_file.read().decode("utf-8")
    st.session_state.doc_text = doc_text

    # Summarize
    with st.spinner("Summarizing document..."):
        summary = summarize_document(doc_text[:8000])
    st.session_state.summary = summary

    # Show summary
    st.subheader("📄 Document Summary (≤ 150 words)")
    st.info(summary)

    # Choose mode
    st.session_state.mode = st.radio("Choose interaction mode:", ["Ask Anything", "Challenge Me"], horizontal=True)

    if st.session_state.mode == "Ask Anything":
        st.subheader("💬 Ask Anything")
        user_q = st.text_input("Enter your question about the document:")
        if user_q:
            with st.spinner("Thinking..."):
                answer = answer_question(st.session_state.doc_text[:8000], user_q)
                snippet = highlight_snippet(st.session_state.doc_text[:8000], answer)
            st.markdown(f"**Answer:** {answer}")
            st.markdown(f"**Supporting Snippet:** \n> {snippet}")

    elif st.session_state.mode == "Challenge Me":
        st.subheader("🧠 Challenge Me")
        if not st.session_state.questions:
            with st.spinner("Generating questions..."):
                q_text = generate_logic_questions(st.session_state.doc_text[:8000])
                questions = []
                for line in q_text.split("\n"):
                    if line.strip().startswith("Q"):
                        questions.append(line.split(":", 1)[-1].strip())
                st.session_state.questions = questions[:3]

        for idx, q in enumerate(st.session_state.questions):
            st.markdown(f"**Q{idx+1}: {q}**")
            user_a = st.text_input(f"Your answer to Q{idx+1}:", key=f"ans_{idx}")
            if user_a:
                with st.spinner("Evaluating..."):
                    feedback = evaluate_answer(st.session_state.doc_text[:8000], q, user_a)
                    snippet = highlight_snippet(st.session_state.doc_text[:8000], feedback)
                st.markdown(f"**Feedback:** {feedback}")
                st.markdown(f"**Supporting Snippet:** \n> {snippet}")

st.markdown("---")
st.caption("🚀 Built with Gemini API for EZ Research Summarization Challenge")
