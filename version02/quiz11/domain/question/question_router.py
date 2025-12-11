from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from domain.question.schemas import QuestionResponse


router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('/list', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db)) -> List[QuestionResponse]:
    questions = db.query(Question).order_by(Question.id.desc()).all()
    return questions


