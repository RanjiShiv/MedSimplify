# app.py

## How to run the app.
# pip install streamlit requests
# python -m streamlit run .\src\python\app.py



import streamlit as st
import requests

SYSTEM_PROMPT = """You are MedSimplify, a plain-language medical explainer.
The user will paste a sanitized medical report or describe symptoms.
Your job is to explain what it means in simple, clear language a non-doctor can understand.
Always:
- Use plain English, no medical jargon.
- Explain what key terms mean.
- Mention what the findings typically indicate (general education only).
- End with: 'This explanation is for educational purposes only. Please consult your doctor.'
Never diagnose. Never recommend specific treatments or medications."""

st.title("MedSimplify — Medical Explainer")
st.caption("Your report stays on your machine. Nothing is sent to the internet.")

report = st.text_area("Paste your medical report or describe your symptoms:", height=200)

if st.button("Explain") and report:
    with st.spinner("Thinking..."):
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "medgemma:latest", # or "llama3.2:3b"
            "system": SYSTEM_PROMPT,
            "prompt": report,
            "stream": False
        })
        st.markdown(response.json()["response"])
        st.warning("This explanation is for educational purposes only. It is not medical advice.")