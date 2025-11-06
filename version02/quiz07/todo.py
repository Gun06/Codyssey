#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI를 사용한 TODO 애플리케이션
CSV 파일을 사용하여 TODO 항목을 저장하고 관리합니다.
"""

import csv
import os
from typing import Any, Dict, List
from fastapi import APIRouter, Body, FastAPI, HTTPException

# CSV 파일 경로
CSV_FILE = 'todo_list.csv'

# APIRouter 인스턴스 생성
router = APIRouter()

# TODO 리스트 (메모리 내 저장)
todo_list: List[Dict[str, Any]] = []


def load_todo_from_csv() -> List[Dict[str, Any]]:
    """
    CSV 파일에서 TODO 항목을 로드합니다.
    
    Returns:
        TODO 항목 리스트
    """
    if not os.path.exists(CSV_FILE):
        return []
    
    loaded_list = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                loaded_list.append(dict(row))
    except Exception:
        return []
    
    return loaded_list


def save_todo_to_csv(todo_items: List[Dict[str, Any]]) -> None:
    """
    TODO 항목을 CSV 파일에 저장합니다.
    
    Args:
        todo_items: 저장할 TODO 항목 리스트
    """
    if not todo_items:
        # 빈 리스트인 경우 파일 삭제
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        return
    
    # CSV 파일의 필드명 결정 (첫 번째 항목의 키를 기준)
    fieldnames = list(todo_items[0].keys())
    
    with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(todo_items)


def is_empty_dict(data: Dict[str, Any]) -> bool:
    """
    Dict가 비어있는지 확인합니다.
    
    Args:
        data: 확인할 Dict 객체
    
    Returns:
        Dict가 비어있으면 True, 아니면 False
    """
    if not isinstance(data, dict):
        return False
    return len(data) == 0


# 애플리케이션 시작 시 CSV에서 데이터 로드
todo_list = load_todo_from_csv()


@router.post('/add_todo')
def add_todo(todo_item: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """
    TODO 항목을 추가합니다.
    
    Args:
        todo_item: 추가할 TODO 항목 (Dict 타입)
    
    Returns:
        추가 결과를 포함한 Dict
    
    Raises:
        HTTPException: 빈 Dict가 입력된 경우
    """
    # 빈 Dict 검증 (보너스 과제)
    if is_empty_dict(todo_item):
        raise HTTPException(
            status_code=400,
            detail='빈 Dict는 입력할 수 없습니다. TODO 항목을 포함한 Dict를 입력해주세요.'
        )
    
    # TODO 항목 추가
    todo_list.append(todo_item)
    
    # CSV 파일에 저장
    save_todo_to_csv(todo_list)
    
    return {
        'status': 'success',
        'message': 'TODO 항목이 추가되었습니다.',
        'todo_item': todo_item,
        'total_count': len(todo_list)
    }


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict[str, Any]:
    """
    TODO 리스트를 가져옵니다.
    
    Returns:
        TODO 리스트를 포함한 Dict
    """
    return {
        'status': 'success',
        'todo_list': todo_list,
        'total_count': len(todo_list)
    }


# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# APIRouter를 애플리케이션에 포함
app.include_router(router)

