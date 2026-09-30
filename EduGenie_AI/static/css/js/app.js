const form = document.getElementById("task-form");
const taskSelect = document.getElementById("task");
const inputText = document.getElementById("input-text");
const resultBox = document.getElementById("result");
const loading = document.getElementById("loading");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const task = taskSelect.value;
    const text = inputText.value.trim();

    if (!text) {
        resultBox.innerHTML = "<p>Please enter some text.</p>";
        return;
    }

    loading.style.display = "block";
    resultBox.innerHTML = "";

    let endpoint;
    let body;

    switch (task) {
        case "qa":
            endpoint = "/qa";
            body = { question: text };
            break;

        case "explain":
            endpoint = "/explain";
            body = { topic: text };
            break;

        case "quiz":
            endpoint = "/quiz";
            body = { text: text };
            break;

        case "summarize":
            endpoint = "/summarize";
            body = { text: text };
            break;

        case "learn":
            endpoint = "/learn/recommendations";
            body = {
                topic: text,
                level: "beginner",
                goal: "Understand the topic clearly"
            };
            break;

        default:
            resultBox.innerHTML = "<p>Invalid task selected.</p>";
            loading.style.display = "none";
            return;
    }

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        console.log("API response:", data);

        if (!response.ok) {
            throw new Error(
                data.detail || "Something went wrong."
            );
        }

        displayResult(task, data);

    } catch (error) {
        console.error(error);

        resultBox.innerHTML = `
            <div class="error">
                <strong>Error:</strong>
                ${escapeHtml(error.message)}
            </div>
        `;
    } finally {
        loading.style.display = "none";
    }
});


function displayResult(task, data) {

    // Q&A
    if (task === "qa") {
        resultBox.innerHTML = `
            <h3>Answer</h3>
            <p>${formatText(data.answer)}</p>
        `;
        return;
    }

    // Explanation
    if (task === "explain") {
        resultBox.innerHTML = `
            <h3>Explanation</h3>
            <div>${formatText(data.explanation)}</div>
        `;
        return;
    }

    // Summary
    if (task === "summarize") {
        resultBox.innerHTML = `
            <h3>Summary</h3>
            <div>${formatText(data.summary)}</div>
        `;
        return;
    }

    // Learning path
    if (task === "learn") {
        resultBox.innerHTML = `
            <h3>Learning Path</h3>
            <div>${formatText(data.recommendations)}</div>
        `;
        return;
    }

    // Quiz
    if (task === "quiz") {
        displayQuiz(data.quiz);
        return;
    }

    resultBox.innerHTML = `
        <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
    `;
}


function displayQuiz(quiz) {

    let questions = quiz;

    // Sometimes the backend returns JSON as a string.
    if (typeof questions === "string") {
        try {
            questions = JSON.parse(questions);
        } catch {
            resultBox.innerHTML = `
                <h3>Quiz</h3>
                <div>${formatText(questions)}</div>
            `;
            return;
        }
    }

    if (!Array.isArray(questions)) {
        resultBox.innerHTML = `
            <h3>Quiz</h3>
            <pre>${escapeHtml(
                JSON.stringify(questions, null, 2)
            )}</pre>
        `;
        return;
    }

    let html = "<h3>Quiz</h3>";

    questions.forEach((item, index) => {

        html += `
            <div class="quiz-question">
                <h4>
                    ${index + 1}. ${escapeHtml(item.question || "")}
                </h4>
        `;

        const options = item.options || [];

        options.forEach((option, optionIndex) => {
            html += `
                <label class="quiz-option">
                    <input
                        type="radio"
                        name="question-${index}"
                        value="${escapeHtml(option)}"
                    >
                    ${escapeHtml(option)}
                </label>
            `;
        });

        html += `
                <button
                    type="button"
                    class="check-answer"
                    onclick="checkAnswer(
                        ${index},
                        '${escapeJs(item.correct_answer || "")}'
                    )"
                >
                    Check Answer
                </button>

                <div
                    id="answer-${index}"
                    class="answer-feedback"
                ></div>

                </div>
        `;
    });

    resultBox.innerHTML = html;
}


function checkAnswer(questionIndex, correctAnswer) {

    const selected = document.querySelector(
        `input[name="question-${questionIndex}"]:checked`
    );

    const feedback = document.getElementById(
        `answer-${questionIndex}`
    );

    if (!selected) {
        feedback.innerHTML = "Please select an answer.";
        return;
    }

    if (selected.value === correctAnswer) {
        feedback.innerHTML = `
            <strong>Correct! ✓</strong>
        `;
    } else {
        feedback.innerHTML = `
            <strong>Incorrect.</strong>
            Correct answer: ${escapeHtml(correctAnswer)}
        `;
    }
}


function formatText(text) {

    if (text === null || text === undefined) {
        return "";
    }

    if (typeof text !== "string") {
        return `
            <pre>${escapeHtml(
                JSON.stringify(text, null, 2)
            )}</pre>
        `;
    }

    return escapeHtml(text)
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");
}


function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function escapeJs(value) {

    return String(value)
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'");
}