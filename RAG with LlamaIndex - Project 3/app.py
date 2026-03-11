import gradio as gr
from config import create_index, load_index, llm
from workflow import RAGWorkflow
import json
import asyncio
from llama_index.core import SimpleDirectoryReader, Settings

# Set global LLM to Cohere
Settings.llm = llm


# Load structured data
with open(".cursor/notes/decisions.md") as f:
    decisions_text = f.read()

# Load or create vector index with Cohere + Pinecone
try:
    vector_index = load_index()
except:
    documents = SimpleDirectoryReader(".cursor/notes").load_data()
    vector_index = create_index(documents)

# Load structured JSON
with open("structured_data.json") as f:
    structured_data = json.load(f)

# Initialize workflow
workflow = RAGWorkflow(vector_index=vector_index, structured_data=structured_data)


async def query_handler(user_query: str) -> str:
    """Handle user query through workflow"""
    result = await workflow.run(query=user_query)
    return result


def gradio_interface(query: str) -> str:
    """Gradio wrapper for async workflow"""
    return asyncio.run(query_handler(query))


# Gradio UI
demo = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(label="שאלה", placeholder="שאל שאלה על המערכת...", rtl=True),
    outputs=gr.Textbox(label="תשובה", rtl=True),
    title="מערכת RAG חכמה",
    description="שאל שאלות על התיעוד הטכני",
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="amber",
    ),
)

if __name__ == "__main__":
    demo.launch()
