import logging
from typing import Dict

from langchain_core.output_parsers import StrOutputParser

from ..prompts import clarification_prompt
from .analysis import initialize_llm


def request_clarification(state: Dict) -> Dict:
    """Generate clarification questions for missing information."""
    logging.info("Generating clarification questions...")

    llm = initialize_llm()
    clarification_chain = clarification_prompt | llm | StrOutputParser()

    questions = clarification_chain.invoke(
        {"missing_info": state["missing_information"]}
    )

    return {**state, "clarification_questions": questions}
