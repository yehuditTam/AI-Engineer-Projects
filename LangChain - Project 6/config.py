import os
from dotenv import load_dotenv

# טעינת משתני הסביבה מקובץ .env
load_dotenv()

# בדיקה בסיסית שהמפתחות אכן נטענו
if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
    raise ValueError("שגיאה: מפתחות ה-API חסרים בקובץ .env! אנא בדקי את ההגדרות.")