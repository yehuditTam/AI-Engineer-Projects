# רשימת המשימות הגלובלית - תשמש כ"מסד הנתונים" שלנו בזיכרון
tasks = []

def get_tasks(status=None, task_type=None):
    """
    שליפת משימות עם אפשרות לסינון לפי סטטוס או סוג.
    """
    filtered_tasks = tasks
    if status:
        filtered_tasks = [t for t in filtered_tasks if t['status'] == status]
    if task_type:
        filtered_tasks = [t for t in filtered_tasks if t['type'] == task_type]
    
    return filtered_tasks

def add_task(code, title, description, task_type, start_date, end_date, status="פתוח"):
    """
    הוספת משימה חדשה למערכת.
    """
    new_task = {
        "code": code,
        "title": title,
        "description": description,
        "type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": status
    }
    tasks.append(new_task)
    return f"המשימה '{title}' (קוד: {code}) נוספה בהצלחה."

def update_task(code, **updates):
    """
    עדכון פרטי משימה קיימת לפי הקוד שלה.
    ניתן לעדכן שדות ספציפיים (כמו סטטוס, תיאור וכו').
    """
    for task in tasks:
        if task['code'] == code:
            task.update(updates)
            return f"משימה {code} ועודכנה בהצלחה."
    return f"שגיאה: משימה עם קוד {code} לא נמצאה."

def delete_task(code):
    """
    מחיקת משימה מהרשימה.
    """
    global tasks
    initial_length = len(tasks)
    tasks = [t for t in tasks if t['code'] != code]
    
    if len(tasks) < initial_length:
        return f"משימה {code} נמחקה בהצלחה."
    return f"שגיאה: משימה עם קוד {code} לא נמצאה."