import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """אתה מומחה לפקודות Windows CMD.
המשימה שלך: להמיר הוראות בשפה טבעית (עברית) לפקודת CMD אחת.

חוקים:
- החזר רק את הפקודה, ללא הסברים
- פקודה אחת בלבד
- תחביר תקין ל-Windows CMD
- אל תוסיף פרמטרים שלא התבקשו במפורש בהוראה

כללי בטיחות:
- אם ההוראה לא ברורה או חסרה מידע קריטי - החזר: "ERROR: הוראה לא ברורה"
- אם יש יותר מפעולה אחת - החזר רק את הפעולה הראשונה
- אל תבצע פעולות מסוכנות (del, rmdir, format) ללא פרטים מדויקים
"""

# Few-shot examples
FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "מה כתובת ה-IP של המחשב שלי"},
    {"role": "assistant", "content": "ipconfig"},
    
    {"role": "user", "content": "הצג את התוכן של התיקייה הנוכחית"},
    {"role": "assistant", "content": "dir"},
    
    {"role": "user", "content": "תמחק את הקבצים הישנים"},
    {"role": "assistant", "content": "ERROR: הוראה לא ברורה"},
    
    {"role": "user", "content": "צור תיקייה בשם backup ואז תעתיק קבצים"},
    {"role": "assistant", "content": "mkdir backup"},
    
    {"role": "user", "content": "מחק את הקובץ test.txt"},
    {"role": "assistant", "content": "del test.txt"},
]


def nl_to_cmd(user_input: str) -> str:
    """ממיר טקסט בשפה טבעית לפקודת CMD"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(FEW_SHOT_EXAMPLES)
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    test_inputs = [
        "מה כתובת ה-IP של המחשב שלי",
        "אני רוצה למחוק את כל הקבצים עם סיומת .tmp בתיקייה downloads",
        "לסדר את רשימת הקבצים לפי גודל מהגדול לקטן",
        "איזה תהליכים רצים כרגע במערכת"
    ]
    
    print("=== בדיקת Agent - גרסה 4 (Few-Shot) ===\n")
    for inp in test_inputs:
        cmd = nl_to_cmd(inp)
        print(f"🗣️  {inp}")
        print(f"💻 {cmd}\n")
