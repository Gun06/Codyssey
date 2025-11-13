#!/usr/bin/env python3
"""
TODO 애플리케이션에서 사용되는 데이터 모델 정의.
"""

from pydantic import BaseModel


class TodoItem(BaseModel):
    """
    TODO 항목을 표현하는 모델.

    Attributes:
        title: TODO 제목.
        description: TODO 상세 설명.
        priority: TODO 우선순위.
    """

    title: str
    description: str
    priority: str

