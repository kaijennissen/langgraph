import logging
from typing import Dict

from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

from ..config import CONFIG
from ..prompts import analyze_requirements_prompt, gap_analysis_prompt


def initialize_llm():
    """Initialize the language model."""
    return ChatOpenAI(
        temperature=CONFIG["llm"]["temperature"], model_name=CONFIG["llm"]["model_name"]
    )


def analyze_requirements(state: Dict) -> Dict:
    """Extract and analyze job requirements."""
    logging.info("Analyzing job requirements...")

    llm = initialize_llm()
    analysis_chain = analyze_requirements_prompt | llm | JsonOutputParser()

    requirements = analysis_chain.invoke({"job_description": state["job_description"]})

    return {**state, "analyzed_requirements": requirements}


def identify_gaps(state: Dict) -> Dict:
    """Identify missing information and areas needing clarification."""
    logging.info("Identifying information gaps...")

    llm = initialize_llm()
    gap_chain = gap_analysis_prompt | llm | JsonOutputParser()

    gaps = gap_chain.invoke(
        {
            "cv_content": state["original_cv"],
            "requirements": state["analyzed_requirements"],
        }
    )

    return {**state, "missing_information": gaps}
