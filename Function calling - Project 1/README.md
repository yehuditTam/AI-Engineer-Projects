# Function Calling - Project 1: AI Task Manager

A conversational task manager powered by an AI agent with function calling capabilities. The agent understands natural language Hebrew commands and performs CRUD operations on tasks.

## Architecture

```
client/index.html  →  FastAPI (main.py)  →  agent_service.py  →  todo_service.py
```

- **main.py** – FastAPI server exposing a `/chat` POST endpoint
- **agent_service.py** – Agent that parses Hebrew natural language and routes to the correct service function
- **todo_service.py** – In-memory task store with get / add / update / delete operations
- **client/index.html** – Browser UI for chatting with the agent

## Getting Started

### Install dependencies

```bash
pip install fastapi uvicorn
```

### Run the server

```bash
python main.py
```

Server runs at `http://127.0.0.1:8000`. Open `client/index.html` in a browser to use the UI.

## API

`POST /chat`

```json
{ "message": "תוסיף משימה לכתוב דוח" }
```

Response:
```json
{ "reply": "המשימה 'לכתוב דוח' (קוד: 1) נוספה בהצלחה." }
```

## Supported Commands (Hebrew)

| Intent | Example |
|--------|---------|
| Add task | `תוסיף משימה לכתוב דוח` |
| List tasks | `מה המשימות שלי?` |
| Update task | `עדכן משימה 1 בוצע` |
| Delete task | `מחק משימה 1` |

> **Note:** Tasks are stored in memory and reset on server restart.
