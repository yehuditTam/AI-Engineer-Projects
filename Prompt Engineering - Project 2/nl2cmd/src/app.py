import gradio as gr
from agent import nl_to_cmd

def convert(user_input: str) -> str:
    if not user_input.strip():
        return ""
    return nl_to_cmd(user_input)

demo = gr.Interface(
    fn=convert,
    inputs=gr.Textbox(label="🗣️ הוראה בשפה טבעית", placeholder="לדוגמה: מה כתובת ה-IP של המחשב שלי"),
    outputs=gr.Textbox(label="💻 פקודת CMD"),
    title="NL2CMD - ממיר שפה טבעית לפקודות CMD",
    examples=[
        ["מה כתובת ה-IP של המחשב שלי"],
        ["אני רוצה למחוק את כל הקבצים עם סיומת .tmp בתיקייה downloads"],
        ["לסדר את רשימת הקבצים לפי גודל מהגדול לקטן"],
        ["איזה תהליכים רצים כרגע במערכת"]
    ]
)

if __name__ == "__main__":
    demo.launch()
