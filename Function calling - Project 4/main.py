from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import agent_service  # ייבוא ה-Agent שיצרנו קודם

# יצירת מופע של FastAPI
app = FastAPI(title="AI Task Manager API")

# הוספת CORS כדי לאפשר גישה מהדפדפן
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת מבנה ההודעה שהשרת מצפה לקבל (Data Model)
class UserRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_agent(request: UserRequest):
    """
    נקודת קצה (Endpoint) שמקבלת הודעה מהלקוח ושולחת אותה ל-Agent.
    """
    # קריאה לפונקציית ה-Agent עם השאילתה מהלקוח
    response = agent_service.agent(request.message)
    
    # החזרת התשובה ללקוח
    return {"reply": response}

# הרצת השרת (אופציונלי להרצה ישירה מהקובץ)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)