from typing import TypedDict

from flask import Blueprint, render_template

from .store import store

bp = Blueprint("routes", __name__)


class Score(TypedDict):
    score: float
    sleeping_confidence: float


@bp.route("/")
def index() -> str:
    return render_template("index.html")


@bp.route("/score")
def score() -> Score:
    status = store.get_status()
    if status is None:
        return Score(score=0.0, sleeping_confidence=0.0)
    return Score(score=status.overall_score, sleeping_confidence=status.sleeping_confidence)
