# 📄 Smart Assistant for Research Summarization

**Task by EZ Labs – GenAI Reasoning Challenge**

## 🚀 Overview

This project implements a **GenAI-powered assistant** capable of:

- Summarizing uploaded documents (PDF/TXT)
- Answering free-form user questions based on document content
- Generating logic-based questions and evaluating user responses
- Justifying all answers with source references
- Providing a clean, web-based UI using **Streamlit**



---

## 🧠 Features

### 📁 Document Upload
- Upload `.pdf` or `.txt` files
- Auto-extract text content

### 📝 Auto Summary
- Generates a concise ≤150-word summary of the document on upload

### 💬 Ask Anything Mode
- Ask any question related to the document
- Assistant provides contextual answers with source-based snippets

### 🧩 Challenge Me Mode
- System asks 3 logic/comprehension-based questions
- User answers → AI evaluates → Justifies with document references

---

## 🛠️ Tech Stack

| Component        | Tool               |
|------------------|--------------------|
| Frontend         | Streamlit          |
| Backend (LLM)    | Google Gemini API  |
| PDF Parser       | PyPDF2             |
| File Handling    | Python 3.11+       |

---


