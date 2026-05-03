import re
import todo_service
from datetime import datetime, timedelta

def agent(query):
    query_lower = query.lower()
    
    # הוספת משימה
    if any(word in query_lower for word in ["תוסיף", "הוסף", "צור", "חדש"]):
        # חילוץ קוד
        code_match = re.search(r'קוד[:\s]*(\d+)', query)
        if not code_match:
            code = str(len(todo_service.tasks) + 1)
        else:
            code = code_match.group(1)
        
        # חילוץ כותרת
        title = query.split("משימה")[-1].split("קוד")[0].strip(": ").strip()
        if not title:
            title = "משימה חדשה"
        
        # תאריכים
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        result = todo_service.add_task(
            code=code,
            title=title,
            description=title,
            task_type="כללי",
            start_date=today,
            end_date=tomorrow,
            status="פתוח"
        )
        return result
    
    # שליפת משימות
    elif any(word in query_lower for word in ["מה", "אילו", "הצג", "רשימה"]):
        tasks = todo_service.get_tasks()
        if not tasks:
            return "אין משימות במערכת"
        
        result = "המשימות שלך:\n"
        for task in tasks:
            result += f"- [{task['code']}] {task['title']} (סטטוס: {task['status']})\n"
        return result
    
    # עדכון משימה
    elif any(word in query_lower for word in ["עדכן", "שנה", "סמן"]):
        code_match = re.search(r'(\d+)', query)
        if code_match:
            code = code_match.group(1)
            status = "בוצע" if "בוצע" in query_lower else "בתהליך"
            result = todo_service.update_task(code, status=status)
            return result
        return "לא מצאתי קוד משימה"
    
    # מחיקת משימה
    elif any(word in query_lower for word in ["מחק", "הסר"]):
        code_match = re.search(r'(\d+)', query)
        if code_match:
            code = code_match.group(1)
            result = todo_service.delete_task(code)
            return result
        return "לא מצאתי קוד משימה"
    
    else:
        return "לא הבנתי. נסה: 'תוסיף משימה...', 'מה המשימות שלי?', 'עדכן משימה X', 'מחק משימה X'"
