# תוצאות בדיקה - גרסה 1

## תרחישי בדיקה

| # | קלט | פלט צפוי | פלט בפועל | סטטוס | הערות |
|---|------|----------|-----------|--------|-------|
| 1 | מה כתובת ה-IP של המחשב שלי | ipconfig | ipconfig | ✅ תקין | |
| 2 | אני רוצה למחוק את כל הקבצים עם סיומת .tmp בתיקייה downloads | del downloads\*.tmp | del downloads\*.tmp /Q | ⚠️ חלקי | הוסיף /Q ללא בקשה |
| 3 | לסדר את רשימת הקבצים לפי גודל מהגדול לקטן | dir /o-s | dir /o-s | ✅ תקין | |
| 4 | איזה תהליכים רצים כרגע במערכת | tasklist | tasklist | ✅ תקין | |
| 5 | הצג את התוכן של התיקייה הנוכחית | dir | dir | ✅ תקין | |
| 6 | צור תיקייה חדשה בשם test | mkdir test | mkdir test | ✅ תקין | |
| 7 | מחק את התיקייה temp | rmdir temp | rmdir temp | ✅ תקין | |
| 8 | העתק את הקובץ file.txt לתיקייה backup | copy file.txt backup\ | copy file.txt backup\ | ✅ תקין | |
| 9 | הצג את כל הקבצים המוסתרים | dir /a:h | dir /a:h | ✅ תקין | |
| 10 | מצא קבצים עם המילה password בשם | dir *password* /s | dir *password* /s | ✅ תקין | |
| 11 | הצג את השעה והתאריך הנוכחיים | date /t && time /t | echo %date% %time% | ❌ שגוי | תחביר שונה |
| 12 | נקה את המסך | cls | cls | ✅ תקין | |
| 13 | הצג את משתני הסביבה | set | set | ✅ תקין | |
| 14 | בדוק את שטח הדיסק הפנוי | wmic logicaldisk get size,freespace | wmic logicaldisk get size,freespace,caption | ⚠️ חלקי | הוסיף caption |
| 15 | הצג את רשימת הדרייברים במחשב | wmic logicaldisk get name | wmic logicaldisk get name | ✅ תקין | |
| 16 | הרוג את התהליך notepad | taskkill /IM notepad.exe | taskkill /IM notepad.exe /F | ⚠️ חלקי | הוסיף /F |
| 17 | הצג את היסטוריית הפקודות | doskey /history | doskey /history | ✅ תקין | |
| 18 | שנה את שם הקובץ old.txt ל-new.txt | ren old.txt new.txt | ren old.txt new.txt | ✅ תקין | |
| 19 | הצג את כל הקבצים שהשתנו היום | forfiles /D 0 /C "cmd /c echo @path" | forfiles /D 0 /C "cmd /c echo @file" | ⚠️ חלקי | @file במקום @path |

## סטטיסטיקה

- **סה"כ תרחישים**: 19
- **תקין**: 13 (68%)
- **חלקי**: 5 (26%)
- **שגוי**: 1 (6%)
- **אחוז הצלחה**: 68%

## בעיות שזוהו

1. **הוספת פרמטרים לא נדרשים** - המודל מוסיף דגלים כמו /Q, /F שלא התבקשו
2. **תחביר חלופי** - משתמש ב-echo %date% במקום date /t
3. **שינויים קלים** - @file במקום @path

## מסקנות לשיפור

**בעיה מרכזית**: המודל מוסיף פרמטרים "חכמים" שלא התבקשו.

**שיפור לגרסה 2**: הוסף כלל מפורש - "אל תוסיף פרמטרים שלא התבקשו במפורש"
