from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    current_level: str = "beginner",
    goal: str = "understand the topic",
    available_time: str = "4 weeks",
) -> str:

    system_instruction = """
You are EduGenie, an educational learning-path assistant.

Create a practical learning path for students.
Organize the response with:
1. Learning objective
2. Recommended topics in order
3. Suggested timeline
4. Practice activities
5. Progress checks
6. Recommended resource types

Keep the plan clear, realistic, and student-friendly.
"""

    prompt = f"""
Create a personalized learning path.

Topic: {topic}
Current level: {current_level}
Learning goal: {goal}
Available time: {available_time}

Provide the learning path in a clear format.
"""

    return generate_text(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.4,
        max_output_tokens=1500,
    )