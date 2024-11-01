from typing import Dict


def format_cv(content: str, template: str = "standard") -> str:
    """Format CV content according to template."""
    # Basic formatting for now - can be expanded with more templates
    sections = content.split("\n\n")
    formatted_content = []

    for section in sections:
        if section.strip():
            formatted_content.append(section.strip())

    return "\n\n".join(formatted_content)


def format_cover_letter(content: str, template: str = "standard") -> str:
    """Format cover letter content according to template."""
    # Basic formatting - can be expanded
    paragraphs = content.split("\n\n")
    formatted_paragraphs = []

    for para in paragraphs:
        if para.strip():
            formatted_paragraphs.append(para.strip())

    return "\n\n".join(formatted_paragraphs)
