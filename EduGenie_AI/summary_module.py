from gemini_client import generate_text


def summarize_text(
    text: str,
    length: str = "medium",
) -> str:

    length_instructions = {
        "short": "Give a very short summary in 3 to 5 sentences.",
        "medium": "Give a clear summary in about 1 to 2 paragraphs.",
        "detailed": "Give a detailed summary covering the important points.",
    }

    instruction = length_instructions.get(
        length.lower(),
        length_instructions["medium"],
    )

    system_instruction = """
You are EduGenie, an educational summarization assistant.

Summarize the provided text accurately and clearly for students.

Rules:
- Keep the important ideas.
- Do not add information that is not present in the original text.
- Use simple, student-friendly language.
- Organize the summary clearly.
- Preserve important terms, concepts, and facts.
"""

    prompt = f"""
Summarize the following text.

Summary length: {length}

{instruction}

TEXT:
{text}

Return only the summary.
"""

    return generate_text(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.3,
        max_output_tokens=1500,
    )