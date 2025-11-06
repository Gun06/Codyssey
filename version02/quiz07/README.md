# FastAPI TODO 애플리케이션

FastAPI를 사용하여 구현한 TODO 애플리케이션입니다. CSV 파일을 사용하여 데이터를 저장하고 관리합니다.

## 설치 및 실행

### 1. 가상환경 활성화

```bash
source venv/bin/activate
```

### 2. 서버 실행

```bash
uvicorn todo:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 `http://localhost:8000`에서 접근할 수 있습니다.

## API 엔드포인트

### 1. TODO 항목 추가 (POST)

**엔드포인트**: `http://localhost:8000/add_todo`

**요청 예시**:

```bash
curl -X POST "http://localhost:8000/add_todo" \
  -H "Content-Type: application/json" \
  -d '{"title": "할 일 1", "description": "첫 번째 할 일", "priority": "high"}'
```

**응답 예시**:

```json
{
  "status": "success",
  "message": "TODO 항목이 추가되었습니다.",
  "todo_item": {
    "title": "할 일 1",
    "description": "첫 번째 할 일",
    "priority": "high"
  },
  "total_count": 1
}
```

### 2. TODO 리스트 조회 (GET)

**엔드포인트**: `http://localhost:8000/retrieve_todo`

**요청 예시**:

```bash
curl -X GET "http://localhost:8000/retrieve_todo"
```

**응답 예시**:

```json
{
  "status": "success",
  "todo_list": [
    {
      "title": "할 일 1",
      "description": "첫 번째 할 일",
      "priority": "high"
    }
  ],
  "total_count": 1
}
```

## 보너스 기능

빈 Dict를 입력하면 400 에러와 함께 경고 메시지가 반환됩니다.

**요청 예시**:

```bash
curl -X POST "http://localhost:8000/add_todo" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**응답 예시**:

```json
{
  "detail": "빈 Dict는 입력할 수 없습니다. TODO 항목을 포함한 Dict를 입력해주세요."
}
```

## 데이터 저장

모든 TODO 항목은 `todo_list.csv` 파일에 저장됩니다. 서버를 재시작해도 데이터가 유지됩니다.

## 요구사항

- Python 3.x
- FastAPI
- uvicorn

## 이슈

프로젝트의 알려진 이슈 및 개선 사항은 [ISSUES.md](ISSUES.md)를 참고하세요.
