import csv
from agent import nl_to_cmd

test_cases = [
    "מה כתובת ה-IP של המחשב שלי",
    "אני רוצה למחוק את כל הקבצים עם סיומת .tmp בתיקייה downloads",
    "לסדר את רשימת הקבצים לפי גודל מהגדול לקטן",
    "איזה תהליכים רצים כרגע במערכת",
    "הצג את התוכן של התיקייה הנוכחית",
    "צור תיקייה חדשה בשם test",
    "מחק את התיקייה temp",
    "העתק את הקובץ file.txt לתיקייה backup",
    "הצג את כל הקבצים המוסתרים",
    "מצא קבצים עם המילה password בשם",
    "הצג את השעה והתאריך הנוכחיים",
    "נקה את המסך",
    "הצג את משתני הסביבה",
    "בדוק את שטח הדיסק הפנוי",
    "הצג את רשימת הדרייברים במחשב",
    "הרוג את התהליך notepad",
    "הצג את היסטוריית הפקודות",
    "שנה את שם הקובץ old.txt ל-new.txt",
    "הצג את כל הקבצים שהשתנו היום"
]

results = []

print("מריץ תרחישי בדיקה...\n")

for i, test_input in enumerate(test_cases, 1):
    print(f"[{i}/{len(test_cases)}] {test_input}")
    try:
        output = nl_to_cmd(test_input)
        results.append({
            "מספר": i,
            "קלט": test_input,
            "פלט": output,
            "סטטוס": "",
            "הערות": ""
        })
        print(f"    → {output}\n")
    except Exception as e:
        results.append({
            "מספר": i,
            "קלט": test_input,
            "פלט": f"ERROR: {str(e)}",
            "סטטוס": "שגוי",
            "הערות": "שגיאה בהרצה"
        })
        print(f"    → ERROR: {e}\n")

with open("test_results.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["מספר", "קלט", "פלט", "סטטוס", "הערות"])
    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ הושלם! התוצאות נשמרו ב-test_results.csv")
print(f"📊 סה\"כ תרחישים: {len(test_cases)}")
