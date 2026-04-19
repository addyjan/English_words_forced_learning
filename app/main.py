from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.session import PracticeSession
from app.storage import WordRepository

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "words.json"

app = FastAPI(title="English Words Forced Learning")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

repo = WordRepository(DATA_FILE)
_sessions: dict[str, PracticeSession] = {}


def get_or_create_session(client_id: str | None) -> tuple[str, PracticeSession]:
    if client_id and client_id in _sessions:
        return client_id, _sessions[client_id]

    new_client_id = str(uuid.uuid4())
    session = PracticeSession(repo.list_words(), repeat_threshold=3)
    _sessions[new_client_id] = session
    return new_client_id, session


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    client_id = request.cookies.get("client_id")
    client_id, session = get_or_create_session(client_id)
    response = templates.TemplateResponse(
        request,
        "index.html",
        {
            "word": session.current(),
            "result": None,
            "progress": session.progress(),
        },
    )
    response.set_cookie("client_id", client_id, httponly=True, samesite="lax")
    return response


@app.post("/submit", response_class=HTMLResponse)
def submit(request: Request, answer: str = Form(...)) -> HTMLResponse:
    client_id = request.cookies.get("client_id")
    client_id, session = get_or_create_session(client_id)
    result = session.submit(answer)

    response = templates.TemplateResponse(
        request,
        "index.html",
        {
            "word": session.current(),
            "result": result,
            "progress": session.progress(),
        },
    )
    response.set_cookie("client_id", client_id, httponly=True, samesite="lax")
    return response


@app.post("/reset")
def reset(request: Request) -> RedirectResponse:
    client_id = request.cookies.get("client_id")
    if client_id and client_id in _sessions:
        del _sessions[client_id]
    return RedirectResponse("/", status_code=303)
