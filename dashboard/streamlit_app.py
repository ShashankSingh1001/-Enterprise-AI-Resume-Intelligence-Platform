import streamlit as st
import requests

# -------------------------
# Config
# -------------------------
API_URL = "http://127.0.0.1:8000/analyze-pdf"

st.set_page_config(
    page_title="AI Resume Screening System",
    layout="centered"
)

# -------------------------
# Header
# -------------------------
st.title("AI Resume Screening System")
st.markdown(
    "Upload a resume and evaluate its match against a job description using AI."
)

st.divider()

# -------------------------
# Inputs
# -------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

jd_text = st.text_area(
    "Job Description",
    height=220,
    placeholder="Paste the job description here..."
)

# -------------------------
# Action Button
# -------------------------
analyze = st.button("Analyze")

# -------------------------
# Processing
# -------------------------
if analyze:

    if uploaded_file is None:
        st.warning("Please upload a resume.")
        st.stop()

    if not jd_text.strip():
        st.warning("Please provide a job description.")
        st.stop()

    with st.spinner("Processing..."):

        try:
            # Prepare request
            file_bytes = uploaded_file.getvalue()

            files = [
                (
                    "file",
                    (
                        uploaded_file.name,
                        file_bytes,
                        "application/pdf"
                    )
                )
            ]

            data = {
                "job_description": jd_text.strip()
            }

            # API call
            response = requests.post(
                API_URL,
                files=files,
                data=data,
                timeout=60
            )

            # Error handling
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}")
                st.stop()

            result = response.json()

            if "match_score" not in result:
                st.error("Invalid response received from API.")
                st.stop()

            # -------------------------
            # Results Section
            # -------------------------
            st.divider()
            st.subheader("Match Analysis")

            score = result["match_score"]
            confidence = result["confidence"]

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Match Score", f"{score}%")

            with col2:
                st.metric("Confidence", f"{confidence:.2f}")

            st.progress(min(int(score), 100))

            # -------------------------
            # Skills Section
            # -------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Matched Skills")
                skills_matched = result.get("skills_matched", [])
                if skills_matched:
                    for skill in skills_matched:
                        st.write(f"- {skill}")
                else:
                    st.write("No strong matches found")

            with col2:
                st.subheader("Missing Skills")
                skills_missing = result.get("skills_missing", [])
                if skills_missing:
                    for skill in skills_missing:
                        st.write(f"- {skill}")
                else:
                    st.write("None")

            # -------------------------
            # Resume Preview
            # -------------------------


        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to backend. Ensure the API server is running.")

        except Exception as e:
            st.error("An unexpected error occurred.")
            st.write(str(e))