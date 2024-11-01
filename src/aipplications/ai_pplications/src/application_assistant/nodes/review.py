import logging
from typing import Dict

from langchain_core.output_parsers import JsonOutputParser

from ..prompts import review_prompt
from .analysis import initialize_llm


def review_documents(state: Dict) -> Dict:
    """Review generated documents for quality and completeness."""
    logging.info("Reviewing generated documents...")

    llm = initialize_llm()
    review_chain = review_prompt | llm | JsonOutputParser()

    review_result = review_chain.invoke(
        {
            "cv": state["tailored_cv"],
            "cover_letter": state["tailored_cover_letter"],
            "requirements": state["analyzed_requirements"],
        }
    )

    return {
        **state,
        "feedback": review_result["feedback"],
        "complete": review_result["complete"],
    }
