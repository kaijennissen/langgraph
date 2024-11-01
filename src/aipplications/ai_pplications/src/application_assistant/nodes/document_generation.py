import logging
from typing import Dict

from langchain_core.output_parsers import StrOutputParser

from ..prompts import cover_letter_prompt, cv_tailoring_prompt
from ..utils.formatting import format_cover_letter, format_cv
from .analysis import initialize_llm


def tailor_cv(state: Dict) -> Dict:
    """Generate tailored CV based on job requirements."""
    logging.info("Tailoring CV...")

    llm = initialize_llm()
    cv_chain = cv_tailoring_prompt | llm | StrOutputParser()

    tailored_content = cv_chain.invoke(
        {
            "original_cv": state["original_cv"],
            "requirements": state["analyzed_requirements"],
            "clarifications": state.get("user_clarifications", {}),
        }
    )

    formatted_cv = format_cv(tailored_content)

    return {**state, "tailored_cv": formatted_cv}


def generate_cover_letter(state: Dict) -> Dict:
    """Generate cover letter based on CV and job requirements."""
    logging.info("Generating cover letter...")

    llm = initialize_llm()
    cover_letter_chain = cover_letter_prompt | llm | StrOutputParser()

    letter_content = cover_letter_chain.invoke(
        {
            "job_description": state["job_description"],
            "requirements": state["analyzed_requirements"],
            "experience": state["tailored_cv"],
        }
    )

    formatted_letter = format_cover_letter(letter_content)

    return {**state, "tailored_cover_letter": formatted_letter}
