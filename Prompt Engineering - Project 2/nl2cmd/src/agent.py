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


def nl_to_cmd(user_input: str) -> str:
    """ממיר טקסט בשפה טבעית לפקודת CMD"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
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
    
    print("=== בדיקת Agent - גרסה ראשונית ===\n")
    for inp in test_inputs:
        cmd = nl_to_cmd(inp)
        print(f"🗣️  {inp}")
        print(f"💻 {cmd}\n")
