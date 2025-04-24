import streamlit as st
import requests

st.set_page_config(page_title="AI Diagnostic Agent", layout="centered")
st.title("🧠 AI Diagnostic Agent")

st.write("Upload a blood report PDF and an X-ray image to get an automated diagnosis.")

blood_file = st.file_uploader("Upload Blood Report (PDF)", type=["pdf"])
xray_file = st.file_uploader("Upload X-ray Image", type=["jpg", "jpeg", "png"])

if st.button("Diagnose"):
    if blood_file and xray_file:
        files = {
            "blood_report": blood_file,
            "xray_image": xray_file,
        }
        with st.spinner("Analyzing..."):
            res = requests.post("http://localhost:8000/diagnose", files=files)
            if res.status_code == 200:
                result = res.json()
                st.subheader("Blood Report Analysis")
                st.json(result["blood_analysis"])
                st.subheader("X-ray Analysis")
                st.json(result["xray_analysis"])
                st.subheader("Diagnosis")
                st.markdown(result["diagnosis"])
            else:
                st.error("Something went wrong. Please check your files and try again.")
    else:
        st.warning("Please upload both files before proceeding.")
