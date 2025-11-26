from datetime import datetime

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base
from database import engine
from database import get_db
from models import Question


Base.metadata.create_all(bind=engine)

app = FastAPI()


class QuestionCreate(BaseModel):
    subject: str
    content: str


@app.get('/')
def read_root() -> dict:
    return {'message': 'quiz09 게시판 API'}


@app.get('/health')
def health_check() -> dict:
    return {'status': 'ok'}


@app.post('/questions')
def create_question(question: QuestionCreate, db: Session = Depends(get_db)) -> dict:
    db_question = Question(
        subject=question.subject,
        content=question.content,
        create_date=datetime.utcnow(),
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return {
        'id': db_question.id,
        'subject': db_question.subject,
        'content': db_question.content,
        'create_date': db_question.create_date.isoformat(),
    }


@app.get('/questions')
def list_questions(db: Session = Depends(get_db)) -> list[dict]:
    questions = db.query(Question).order_by(Question.id.desc()).all()
    return [
        {
            'id': q.id,
            'subject': q.subject,
            'content': q.content,
            'create_date': q.create_date.isoformat(),
        }
        for q in questions
    ]


@app.get('/questions/{question_id}')
def get_question(question_id: int, db: Session = Depends(get_db)) -> dict:
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Question not found')
    return {
        'id': question.id,
        'subject': question.subject,
        'content': question.content,
        'create_date': question.create_date.isoformat(),
    }



