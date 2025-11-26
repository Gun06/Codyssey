from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question


router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('/list')
def question_list(db: Session = Depends(get_db)) -> List[dict]:
    questions = db.query(Question).order_by(Question.id.desc()).all()
    return [
        {
            'id': question.id,
            'subject': question.subject,
            'content': question.content,
            'create_date': question.create_date.isoformat(),
        }
        for question in questions
    ]


