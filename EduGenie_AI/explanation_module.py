from gemini_client import generate_text


def explain_topic(
    topic: str,
    level: str = "beginner",
) -> str:
    """
    Generate a simple educational explanation for a topic.
    """

    system_instruction = """
You are EduGenie, an AI educational assistant.

Explain topics clearly and accurately for students.

Rules:
- Use simple and easy-to-understand language.
- Adjust the explanation to the student's level.
- Start with a clear definition.
- Explain the main concepts step by step.
- Give a simple real-life example when useful.
- Use headings and bullet points when they improve clarity.
- Do not add unrelated information.
"""

    prompt = f"""
Explain the following topic:

Topic: {topic}
Student level: {level}

Create a clear, student-friendly explanation.
"""

    return generate_text(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.4,
        max_output_tokens=1500,
    )