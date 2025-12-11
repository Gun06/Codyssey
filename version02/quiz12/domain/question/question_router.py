from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from domain.question.schemas import QuestionCreate
from domain.question.schemas import QuestionResponse


router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.post('/create', response_model=QuestionResponse)
def question_create(
    question: QuestionCreate, db: Session = Depends(get_db)
) -> QuestionResponse:
    db_question = Question(
        subject=question.subject,
        content=question.content,
        create_date=datetime.utcnow(),
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

