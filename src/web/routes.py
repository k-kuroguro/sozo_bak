from typing import TypedDict

from flask import Blueprint, render_template

from .store import store

bp = Blueprint("routes", __name__)


class ConcentrationStatus(TypedDict):
    overall_score: float
    sleeping_confidence: float


@bp.route("/")
def index() -> str:
    return render_template("index.html")


@bp.route("/concentration_status")
def concentration_status() -> ConcentrationStatus:
    status = store.get_status()
    if status is None:
        return ConcentrationStatus(overall_score=-1.0, sleeping_confidence=-1.0)
    return ConcentrationStatus(
        overall_score=status.overall_score, sleeping_confidence=status.sleeping_confidence
    )
