import config  # טוען אוטומטית את מפתחות ה-API
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver  # רכיב הזיכרון

# 1. הנחיית המערכת (System Prompt)
# נבקש מהסוכן במפורש לעצור ולהציג את המקורות לפני שהוא מסכם אותם
SYSTEM_PROMPT = """You are an expert research assistant modeled after NotebookLM.
Your primary goal is to gather high-quality, diverse information sources on a given topic requested by the user.

Guidelines:
1. Use the search tool to find relevant web pages, articles, and documentation.
2. Formulate your response as a list of potential sources, including Title, URL, and a short Description.
3. Explicitly ask the user to approve or reject these sources before proceeding to any summary."""

# 2. אתחול הרכיבים
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]

# 3. הוספת ניהול הזיכרון (Checkpointer)
# ה-Checkpointer שומר את מצב הגרף ומאפשר לנו לעצור ולהמשיך
memory = MemorySaver()

# 4. יצירת הסוכן עם נקודת עצירה מובנית
# אנחנו מנחים את הגרף לבצע interrupt (עצירה) מיד לאחר שהסוכן (the model) 
# מחליט להפעיל כלי או להחזיר את תוצאות החיפוש, או פשוט לעצור לפני הפעלת הכלים.
# לצורך פשטות ה-HITL, נעצור ברגע שהמודל מבקש להפעיל את כלי החיפוש (tools)
agent = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=SYSTEM_PROMPT,
    checkpointer=memory,
    interrupt_after=["tools"]  # עוצר מיד לאחר שכלי החיפוש הופעל והחזיר נתונים לגרף
)

# 5. פונקציה לניהול זרימת ה-Human in the Loop
def run_research_with_hitl(topic: str):
    # הגדרת מזהה ייחודי לשיחה הזו (Thread) - חיוני עבור רכיב הזיכרון
    config_thread = {"configurable": {"thread_id": "research_session_1"}}
    
    print(f"🔎 שלב 1: מתחיל לחקור את הנושא: '{topic}'...\n")
    inputs = {"messages": [("user", f"Please research this topic: {topic}")]}
    
    # ריצה ראשונה - הסוכן ירוץ, יפעיל את Tavily, ויעצר מיד לאחר מכן בגלל ה-interrupt_after
    for event in agent.stream(inputs, config_thread, stream_mode="values"):
        pass  # מריץ את הגרף עד לנקודת העצירה
    
    # שליפת המצב הנוכחי כדי לראות מה הסוכן מצא
    current_state = agent.get_state(config_thread)
    last_message = current_state.values["messages"][-1]
    
    print("\n=== 🛑 נקודת עצירה: המקורות הגולמיים שהתקבלו מ-Tavily ===")
    print("הסוכן אסף את המידע הבא מהאינטרנט. כעת תורך לאשר:")
    print(last_message.content)
    print("========================================================\n")
    
    # 6. קבלת פידבק מהמשתמש (Human Input)
    user_feedback = input("האם המקורות האלו מתאימים? רשמי את הערותיך או אשרי (למשל: 'אשר הכל' או 'תתעלם ממקור 2'): ")
    
    print("\n🚀 שלב 2: ממשיך את ריצת הסוכן עם המשוב שלך...\n")
    
    # שליחת התגובה של המשתמש כהמשך ישיר בריצה (Resume)
    # אנחנו משתמשים ב-invoke ומעבירים רק את הודעת המשתמש החדשה תחת אותו thread_id
    resume_inputs = {"messages": [("user", f"Here is my feedback on the sources: {user_feedback}. Now please provide the final organized list based on my choice.")]}
    
    final_result = agent.invoke(resume_inputs, config_thread)
    
    print("=== 📋 תוצאות סופיות לאחר סינון אנושי ===")
    print(final_result["messages"][-1].content)

# הרצה לבדיקת שלב ב'
if __name__ == "__main__":
    run_research_with_hitl("What are the main new features in Angular 18 and 19?")