from datetime import datetime

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        orm_mode = True

