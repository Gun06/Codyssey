from fastapi import FastAPI

from database import Base
from database import engine
from domain.question.question_router import router as question_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def read_root() -> dict:
    return {'message': 'quiz12 게시판 API'}


@app.get('/health')
def health_check() -> dict:
    return {'status': 'ok'}


app.include_router(question_router)

