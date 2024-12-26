from typing import Literal

from pydantic import BaseModel


class QuestionAnswer(BaseModel):
    question_id: int
    answer: int


class AnswerFeedback(BaseModel):
    feedback: Literal["KO", "OK"]
