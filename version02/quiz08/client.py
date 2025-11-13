#!/usr/bin/env python3
"""
FastAPI TODO 애플리케이션을 호출하는 간단한 클라이언트.

표준 라이브러리의 urllib을 사용하여 서버와 통신합니다.
"""

import json
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = 'http://127.0.0.1:8000'


def _perform_request(request: Request) -> Dict[str, Any]:
    """
    HTTP 요청을 수행하고 JSON 응답을 Dict로 반환합니다.

    Args:
        request: 실행할 Request 객체.

    Returns:
        JSON 응답을 Dict로 변환한 결과.
    """

    try:
        with urlopen(request, timeout=10) as response:
            response_body = response.read().decode('utf-8')
            if not response_body:
                return {}
            return json.loads(response_body)
    except HTTPError as exc:
        return {'status': 'error', 'code': exc.code, 'reason': exc.reason}
    except URLError as exc:
        return {'status': 'error', 'reason': str(exc.reason)}


def create_todo(title: str, description: str, priority: str) -> Dict[str, Any]:
    """
    TODO 항목을 생성합니다.
    """

    payload = json.dumps(
        {'title': title, 'description': description, 'priority': priority}
    ).encode('utf-8')
    request = Request(
        url=f'{BASE_URL}/todos',
        method='POST',
        data=payload,
        headers={'Content-Type': 'application/json'},
    )
    return _perform_request(request)


def list_todos() -> Dict[str, Any]:
    """
    TODO 항목 리스트를 조회합니다.
    """

    request = Request(url=f'{BASE_URL}/todos', method='GET')
    return _perform_request(request)


def retrieve_todo(todo_id: int) -> Dict[str, Any]:
    """
    단일 TODO 항목을 조회합니다.
    """

    request = Request(url=f'{BASE_URL}/todos/{todo_id}', method='GET')
    return _perform_request(request)


def modify_todo(todo_id: int, title: str, description: str, priority: str) -> Dict[str, Any]:
    """
    TODO 항목을 수정합니다.
    """

    payload = json.dumps(
        {'title': title, 'description': description, 'priority': priority}
    ).encode('utf-8')
    request = Request(
        url=f'{BASE_URL}/todos/{todo_id}',
        method='PUT',
        data=payload,
        headers={'Content-Type': 'application/json'},
    )
    return _perform_request(request)


def remove_todo(todo_id: int) -> Dict[str, Any]:
    """
    TODO 항목을 삭제합니다.
    """

    request = Request(url=f'{BASE_URL}/todos/{todo_id}', method='DELETE')
    return _perform_request(request)


def main() -> None:
    """
    간단한 실행 예제.
    """

    print('=== TODO 생성 ===')
    created = create_todo('샘플 TODO', '클라이언트에서 생성한 항목', 'high')
    print(created)

    print('=== 전체 조회 ===')
    print(list_todos())

    if created.get('id'):
        todo_id = int(created['id'])
        print('=== 단일 조회 ===')
        print(retrieve_todo(todo_id))

        print('=== 수정 ===')
        print(modify_todo(todo_id, '수정된 TODO', '설명도 함께 수정', 'medium'))

        print('=== 삭제 ===')
        print(remove_todo(todo_id))


if __name__ == '__main__':
    main()

