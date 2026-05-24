import streamlit as st
import config  # טעינת מפתחות ה-API
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# --- הגדרות דף וכותרת המערכת ---
st.set_page_config(page_title="NotebookLM Clone", page_icon="🏗️", layout="centered")
st.title("🏗️ NotebookLM - Agent Explorer")
st.write("הזיני נושא, והסוכן האוטונומי יחפש מקורות מידע וימתין לאישורך!")

# --- אתחול רכיבי הליבה (פעם אחת בלבד כדי לחסוך בזיכרון) ---
@st.cache_resource
def init_agent():
    SYSTEM_PROMPT = """You are an expert research assistant modeled after NotebookLM.
    Your primary goal is to gather high-quality, diverse information sources on a given topic requested by the user.
    Use the search tool to find web pages, and then clearly present them so the user can choose which ones to use."""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    search_tool = TavilySearchResults(max_results=4)
    memory = MemorySaver()
    
    # יצירת הסוכן עם נקודת עצירה מיד לאחר הפעלת הכלים
    agent_instance = create_react_agent(
    model=llm,
    tools=[search_tool],
    prompt=SYSTEM_PROMPT,  # השתמשי ב-prompt במקום state_modifier
    checkpointer=memory,
    interrupt_after=["tools"]
)
    return agent_instance

agent = init_agent()

# --- ניהול מצב האפליקציה (Streamlit Session State) ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit_session_unique_1"
if "step" not in st.session_state:
    st.session_state.step = "input"  # השלבים: input -> review -> final
if "raw_results" not in st.session_state:
    st.session_state.raw_results = ""

config_thread = {"configurable": {"thread_id": st.session_state.thread_id}}

# --- שלב 1: הזנת נושא המחקר ---
if st.session_state.step == "input":
    topic = st.text_input("על איזה נושא תרצי לעשות מחקר?", placeholder="לדוגמה: New features in Angular 19")
    
    if st.button("צא לדרך 🚀", use_container_width=True):
        if topic:
            with st.spinner("הסוכן סורק את הרשת ומקבץ מקורות מידע..."):
                # הרצה ראשונית עד לנקודת העצירה (interrupt)
                inputs = {"messages": [("user", f"Please research this topic: {topic}")]}
                agent.invoke(inputs, config_thread)
                
                # שליפת המקורות שנמצאו מתוך ה-State
                current_state = agent.get_state(config_thread)
                st.session_state.raw_results = current_state.values["messages"][-1].content
                st.session_state.step = "review"
                st.rerun()
        else:
            st.warning("אנא הזני נושא למחקר!")

# --- שלב 2: Human in the Loop (בחירה ואישור מקורות) ---
elif st.session_state.step == "review":
    st.subheader("🛑 נקודת ביקורת: המקורות שהסוכן מצא")
    st.info("קראי את המקורות שנמצאו ובחרי כיצד להמשיך:")
    
    # הצגת התוצאות שהסוכן אסף מהרשת
    st.text_area("מקורות גולמיים מהרשת:", value=st.session_state.raw_results, height=250, disabled=True)
    
    # תיבת קלט להנחיות הסינון של המשתמש
    user_feedback = st.text_area(
        "הנחיות לסינון (למשל: 'תאשר רק את המקורות הרשמיים' או 'אשר הכל חוץ מהשני')",
        value="אשר את כל המקורות ומזג אותם לסיכום מקיף."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("אשר והמשך לסיכום 📑", use_container_width=True):
            with st.spinner("הסוכן מעבד את המקורות המאושרים ומנסח סיכום..."):
                # שליחת הפידבק והמשך הריצה (Resume) מהנקודה שבה עצרנו
                resume_inputs = {"messages": [("user", f"Here is my feedback: {user_feedback}. Now compile the final summary.")]}
                final_result = agent.invoke(resume_inputs, config_thread)
                
                # שמירת התוצאה הסופית ומעבר לשלב הבא
                st.session_state.final_summary = final_result["messages"][-1].content
                st.session_state.step = "final"
                st.rerun()
                
    with col2:
        if st.button("התחל מחקר חדש 🔄", use_container_width=True):
            # איפוס המצב
            st.session_state.step = "input"
            st.session_state.raw_results = ""
            st.rerun()

# --- שלב 3: הצגת תוצר סופי וסיכום ראשוני ---
elif st.session_state.step == "final":
    st.subheader("📋 הסיכום הראשוני של ה-Agent")
    st.success("המחקר הושלם בהצלחה על בסיס המקורות שאושרו!")
    
    # הצגת התוצר הסופי בצורת מרקדאון מעוצב
    st.markdown(st.session_state.final_summary)
    
    st.write("---")
    if st.button("בצע מחקר בנושא חדש 🔎", use_container_width=True):
        st.session_state.step = "input"
        st.session_state.raw_results = ""
        st.rerun()