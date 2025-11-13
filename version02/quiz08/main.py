#!/usr/bin/env python3
"""
FastAPI 기반 TODO 애플리케이션.

CSV 파일을 이용하여 TODO 데이터를 저장하고 관리합니다.
"""

import csv
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException

from model import TodoItem

# CSV 파일 경로
CSV_FILE_PATH = Path(__file__).with_name('todo_list.csv')

app = FastAPI()

# 메모리 상의 TODO 리스트
todo_items: List[Dict[str, str]] = []


def load_todo_items() -> List[Dict[str, str]]:
    """
    CSV 파일에서 TODO 항목을 로드합니다.

    Returns:
        TODO 항목 리스트.
    """

    if not CSV_FILE_PATH.exists():
        return []

    loaded_items: List[Dict[str, str]] = []
    highest_id = 0

    try:
        with CSV_FILE_PATH.open('r', encoding='utf-8') as file_pointer:
            reader = csv.DictReader(file_pointer)
            for row in reader:
                current_id = row.get('id')
                if current_id is None or not current_id.isdigit():
                    highest_id += 1
                    current_id = str(highest_id)
                else:
                    numeric_id = int(current_id)
                    if numeric_id > highest_id:
                        highest_id = numeric_id
                loaded_items.append(
                    {
                        'id': current_id,
                        'title': row.get('title', ''),
                        'description': row.get('description', ''),
                        'priority': row.get('priority', ''),
                    }
                )
    except (OSError, csv.Error) as exc:
        raise HTTPException(status_code=500, detail=f'CSV 파일을 읽는 중 오류가 발생했습니다: {exc}') from exc

    return loaded_items


def save_todo_items(items: List[Dict[str, str]]) -> None:
    """
    TODO 항목을 CSV 파일에 저장합니다.

    Args:
        items: 저장할 TODO 항목 리스트.
    """

    fieldnames = ['id', 'title', 'description', 'priority']

    try:
        with CSV_FILE_PATH.open('w', encoding='utf-8', newline='') as file_pointer:
            writer = csv.DictWriter(file_pointer, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(
                    {
                        'id': item.get('id', ''),
                        'title': item.get('title', ''),
                        'description': item.get('description', ''),
                        'priority': item.get('priority', ''),
                    }
                )
    except (OSError, csv.Error) as exc:
        raise HTTPException(status_code=500, detail=f'CSV 파일을 저장하는 중 오류가 발생했습니다: {exc}') from exc


def generate_new_id(items: List[Dict[str, str]]) -> str:
    """
    새 TODO 항목을 위한 ID를 발급합니다.

    Args:
        items: 현재 저장된 TODO 항목 리스트.

    Returns:
        새로 생성된 ID 문자열.
    """

    if not items:
        return '1'

    numeric_ids = [int(item['id']) for item in items if item.get('id', '').isdigit()]
    next_id = max(numeric_ids) + 1 if numeric_ids else 1
    return str(next_id)


def find_todo_index(todo_id: str) -> int:
    """
    ID로 TODO 항목 인덱스를 조회합니다.

    Args:
        todo_id: 조회할 TODO ID.

    Returns:
        리스트에서 해당 TODO 항목의 인덱스. 존재하지 않을 경우 -1.
    """

    for index, item in enumerate(todo_items):
        if item.get('id') == todo_id:
            return index
    return -1


@app.on_event('startup')
def startup_event() -> None:
    """
    애플리케이션 시작 시 CSV 데이터를 로드합니다.
    """

    global todo_items
    todo_items = load_todo_items()


@app.post('/todos')
def add_todo(todo_item: TodoItem) -> Dict[str, str]:
    """
    TODO 항목을 추가합니다.

    Args:
        todo_item: 추가할 TODO 항목.

    Returns:
        추가된 TODO 항목 정보.
    """

    new_id = generate_new_id(todo_items)
    created_item = {
        'id': new_id,
        'title': todo_item.title,
        'description': todo_item.description,
        'priority': todo_item.priority,
    }

    todo_items.append(created_item)
    save_todo_items(todo_items)

    return created_item


@app.get('/todos')
def retrieve_todo() -> Dict[str, List[Dict[str, str]]]:
    """
    TODO 리스트를 반환합니다.

    Returns:
        현재 TODO 항목 리스트.
    """

    return {'todos': todo_items}


@app.get('/todos/{todo_id}')
def get_single_todo(todo_id: int) -> Dict[str, str]:
    """
    단일 TODO 항목을 반환합니다.

    Args:
        todo_id: 조회할 TODO 항목의 ID.

    Returns:
        TODO 항목 정보.
    """

    todo_index = find_todo_index(str(todo_id))
    if todo_index == -1:
        raise HTTPException(status_code=404, detail='해당 ID의 TODO 항목을 찾을 수 없습니다.')

    return todo_items[todo_index]


@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo_item: TodoItem) -> Dict[str, str]:
    """
    TODO 항목을 수정합니다.

    Args:
        todo_id: 수정할 TODO 항목의 ID.
        todo_item: 수정될 TODO 항목 데이터.

    Returns:
        수정된 TODO 항목 정보.
    """

    todo_index = find_todo_index(str(todo_id))
    if todo_index == -1:
        raise HTTPException(status_code=404, detail='해당 ID의 TODO 항목을 찾을 수 없습니다.')

    updated_item = {
        'id': str(todo_id),
        'title': todo_item.title,
        'description': todo_item.description,
        'priority': todo_item.priority,
    }

    todo_items[todo_index] = updated_item
    save_todo_items(todo_items)

    return updated_item


@app.delete('/todos/{todo_id}')
def delete_single_todo(todo_id: int) -> Dict[str, str]:
    """
    TODO 항목을 삭제합니다.

    Args:
        todo_id: 삭제할 TODO 항목의 ID.

    Returns:
        삭제 결과 메시지.
    """

    todo_index = find_todo_index(str(todo_id))
    if todo_index == -1:
        raise HTTPException(status_code=404, detail='해당 ID의 TODO 항목을 찾을 수 없습니다.')

    removed_item = todo_items.pop(todo_index)
    save_todo_items(todo_items)

    return {'message': f"ID {removed_item.get('id')} TODO 항목이 삭제되었습니다."}

