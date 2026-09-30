from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import (
    ErrorResponse,
    ExplainRequest,
    LearningPathRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
)

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # AI clients/models are loaded lazily.
    yield


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description=(
        "An educational assistant for Q&A, explanations, "
        "quizzes, summaries, and learning paths."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/health", tags=["system"])
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


@app.post(
    "/qa",
    tags=["AI"],
    responses={500: {"model": ErrorResponse}}
)
async def qa(payload: QARequest):
    try:
        result = answer_question(payload.question)

        return {
            "answer": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@app.post(
    "/explain",
    tags=["AI"],
    responses={500: {"model": ErrorResponse}}
)
async def explain(payload: ExplainRequest):
    try:
        result = explain_topic(payload.topic)

        return {
            "explanation": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@app.post(
    "/quiz",
    tags=["AI"],
    responses={500: {"model": ErrorResponse}}
)
async def quiz(payload: QuizRequest):
    try:
        result = generate_quiz(payload.text)

        return {
            "quiz": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@app.post(
    "/summarize",
    tags=["AI"],
    responses={500: {"model": ErrorResponse}}
)
async def summarize(payload: SummaryRequest):
    try:
        result = summarize_text(payload.text)

        return {
            "summary": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


@app.post(
    "/learn/recommendations",
    tags=["AI"],
    responses={500: {"model": ErrorResponse}}
)
async def learning_recommendations(
    payload: LearningPathRequest
):
    try:
        result = get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.goal,
        )

        return {
            "recommendations": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc