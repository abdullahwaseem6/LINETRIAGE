"""Second opinion on safety from the small model trained in training/train_baseline.py.

It never decides the route: rules.py does. It only flags notes where the small
model sees danger, so a human can double-check. Returns None if no model has
been trained yet (models/ is not in git; run training/train_baseline.py).
"""

import time
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "baseline.joblib"


class SecondOpinion(BaseModel):
    danger_score: float
    threshold: float
    dangerous: bool
    milliseconds: float


@lru_cache(maxsize=1)
def _load():
    if not MODEL_PATH.exists():
        return None
    import joblib

    return joblib.load(MODEL_PATH)


def second_opinion(text: str) -> SecondOpinion | None:
    model = _load()
    if model is None:
        return None
    start = time.perf_counter()
    score = float(model["safety"].predict_proba([text])[0, 1])
    return SecondOpinion(
        danger_score=round(score, 3),
        threshold=model["threshold"],
        dangerous=score >= model["threshold"],
        milliseconds=round((time.perf_counter() - start) * 1000, 2),
    )
