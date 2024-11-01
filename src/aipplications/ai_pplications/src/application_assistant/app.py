import logging

import streamlit as st

from .graph import create_application_assistant
from .utils.parsing import process_document

logging.basicConfig(level=logging.INFO)


def handle_clarification(questions: str) -> dict:
    """Handle user clarifications through Streamlit interface."""
    st.subheader("Additional Information Needed")
    st.write(questions)

    responses = {}
    user_input = st.text_area("Please provide the requested information:")

    if user_input:
        responses["user_response"] = user_input

    return responses


def main():
    st.title("Application Document Assistant")

    # Initialize session state
    if "assistant" not in st.session_state:
        st.session_state.assistant = create_application_assistant()
        st.session_state.current_state = None

    # File uploads
    with st.form("document_upload"):
        cv_file = st.file_uploader("Upload your CV", type=["pdf", "docx"])
        job_desc_file = st.file_uploader(
            "Upload Job Description", type=["pdf", "docx", "txt"]
        )
        cover_letter_file = st.file_uploader(
            "Upload Cover Letter (optional)", type=["pdf", "docx"]
        )

        submitted = st.form_submit_button("Generate Documents")

    if submitted and cv_file and job_desc_file:
        with st.spinner("Processing documents..."):
            try:
                # Initialize state
                initial_state = {
                    "original_cv": process_document(cv_file),
                    "job_description": process_document(job_desc_file),
                    "original_cover_letter": (
                        process_document(cover_letter_file)
                        if cover_letter_file
                        else None
                    ),
                    "analyzed_requirements": [],
                    "missing_information": [],
                    "user_clarifications": {},
                    "tailored_cv": "",
                    "tailored_cover_letter": "",
                    "feedback": "",
                    "complete": False,
                }

                # Run the graph
                result = st.session_state.assistant.invoke(initial_state)

                # Handle clarifications if needed
                if "clarification_questions" in result:
                    user_responses = handle_clarification(
                        result["clarification_questions"]
                    )
                    if user_responses:
                        result["user_clarifications"] = user_responses
                        result = st.session_state.assistant.invoke(result)

                # Display results
                st.subheader("Tailored CV")
                st.text_area("", value=result["tailored_cv"], height=300)

                st.subheader("Cover Letter")
                st.text_area("", value=result["tailored_cover_letter"], height=300)

                # Add download buttons
                st.download_button(
                    "Download CV", result["tailored_cv"], file_name="tailored_cv.txt"
                )
                st.download_button(
                    "Download Cover Letter",
                    result["tailored_cover_letter"],
                    file_name="cover_letter.txt",
                )

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                st.error(f"An error occurred while processing your documents: {str(e)}")


if __name__ == "__main__":
    main()
