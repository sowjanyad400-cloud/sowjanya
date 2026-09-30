from gemini_client import generate_text
import json


def clean_json_block(text: str) -> str:
    """Remove Markdown code fences if Gemini returns JSON inside them."""
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text


def generate_quiz(text: str):
    prompt = f"""
Create a quiz based on the following topic/text:

{text}

Generate exactly 3 multiple-choice questions.

Each question must contain:
- question
- 4 options
- correct_answer

Return ONLY valid JSON in this format:

[
  {{
    "question": "Question 1",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A"
  }},
  {{
    "question": "Question 2",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option B"
  }},
  {{
    "question": "Question 3",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option C"
  }}
]
"""

    result = generate_text(
        prompt=prompt,
        system_instruction="""
You are EduGenie, an educational quiz generator.
Create clear and student-friendly multiple-choice questions.
Always return valid JSON only.
""",
        temperature=0.4,
        max_output_tokens=1500,
    )

    cleaned = clean_json_block(result)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "Quiz generation returned invalid JSON.",
            "raw_response": result
        }