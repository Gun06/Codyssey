from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class QuestionCreate(BaseModel):
    subject: str = Field(..., min_length=1, description='질문 제목')
    content: str = Field(..., min_length=1, description='질문 내용')


class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        orm_mode = True

