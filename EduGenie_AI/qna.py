from gemini_client import generate_text


def offline_answer(question: str) -> str:
    q = question.lower().strip()

    # Python
    if "what is python" in q or q == "python":
        return """
Python is a high-level, interpreted, general-purpose programming language.
It is popular because its syntax is simple, readable, and easy to learn.

Main features of Python:
1. Easy to learn and use
2. High-level programming language
3. Interpreted language
4. Object-oriented programming support
5. Large collection of libraries
6. Portable and cross-platform

Uses of Python:
- Web development
- Artificial Intelligence
- Machine Learning
- Data Science
- Automation
- Scientific computing

Example:
Python can be used to create websites, analyze data, automate tasks,
and develop AI applications.
"""

    # OOP
    if (
        "what is oop" in q
        or "object oriented programming" in q
        or "object-oriented programming" in q
    ):
        return """
Object-Oriented Programming (OOP) is a programming approach that
organizes a program using classes and objects.

Main concepts of OOP:

1. Class
A class is a blueprint for creating objects.

2. Object
An object is an instance of a class.

3. Encapsulation
Encapsulation combines data and methods into a single unit.

4. Inheritance
Inheritance allows a new class to reuse properties and methods
of an existing class.

5. Polymorphism
Polymorphism allows the same operation to behave differently
in different situations.

6. Abstraction
Abstraction hides unnecessary implementation details and shows
only the important information.

Real-life example:
A Car can be considered an object.

Properties:
- Colour
- Model
- Speed

Functions:
- Start
- Stop
- Accelerate
"""

    # C++
    if "what is c++" in q or q == "c++":
        return """
C++ is a general-purpose programming language developed as an
extension of the C programming language.

Important features of C++:
1. Object-oriented programming
2. Classes and objects
3. Inheritance
4. Polymorphism
5. Encapsulation
6. Abstraction
7. Function and operator overloading

C++ is commonly used for software development, game development,
system programming, embedded systems, and high-performance applications.
"""

    # AI
    if "what is ai" in q or "artificial intelligence" in q:
        return """
Artificial Intelligence (AI) is a branch of computer science that
enables computers and machines to perform tasks that normally require
human intelligence.

Examples of AI tasks include:
1. Learning
2. Problem solving
3. Understanding language
4. Recognizing images
5. Making decisions

Applications of AI include:
- Chatbots
- Recommendation systems
- Self-driving technology
- Medical analysis
- Education
- Voice assistants
"""

    # Machine Learning
    if "machine learning" in q:
        return """
Machine Learning (ML) is a branch of Artificial Intelligence in which
computers learn patterns from data and use those patterns to make
predictions or decisions.

Main types of Machine Learning:
1. Supervised Learning
2. Unsupervised Learning
3. Reinforcement Learning

Applications include:
- Recommendation systems
- Image recognition
- Spam detection
- Prediction systems
- Speech recognition
"""

    # Computer
    if "what is computer" in q:
        return """
A computer is an electronic device that accepts data as input,
processes the data according to instructions, stores information,
and produces output.

Basic functions of a computer:
1. Input
2. Processing
3. Storage
4. Output

Examples of computers include desktops, laptops, tablets,
and servers.
"""

    # Internet
    if "what is internet" in q:
        return """
The Internet is a worldwide network that connects computers and
other devices so they can communicate and share information.

The Internet is used for:
- Communication
- Education
- Online shopping
- Banking
- Entertainment
- Information sharing
"""

    # Database
    if "what is database" in q:
        return """
A database is an organized collection of data that can be stored,
managed, searched, and updated efficiently.

Examples of database systems include:
- MySQL
- PostgreSQL
- Oracle
- Microsoft SQL Server

Databases are commonly used in websites, banking systems,
college management systems, and business applications.
"""

    # Default useful answer
    return f"""
EduGenie Offline Answer

Your question:
{question}

This question requires a detailed AI-generated response.

Gemini is currently unavailable because its API quota has been
reached, so EduGenie is answering using its offline knowledge base.

Please try asking about common programming, computer science,
Python, C++, AI, Machine Learning, OOP, databases, or Internet
concepts.
"""


def answer_question(question: str) -> str:

    try:
        return generate_text(
            prompt=f"""
Answer this student's question clearly and simply:

{question}
""",
            system_instruction="""
You are EduGenie, an educational AI assistant.
Give accurate, student-friendly explanations.
Use headings, bullet points, and examples when useful.
""",
            temperature=0.4,
            max_output_tokens=1200,
        )

    except Exception as exc:

        error_text = str(exc)

        # Gemini quota / temporary availability
        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):
            return offline_answer(question)

        raise