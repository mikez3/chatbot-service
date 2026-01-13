import uuid
import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
from llm import generate_response, generate_response_no_memory 

app = FastAPI(root_path = "/uniche")

class ChatMessage(BaseModel):
    message: str
    session_id: str | None = None  # Optional, in request body

@app.post("/chat_with_userID")
def chat(request: ChatMessage):
    session_id = request.session_id or str(uuid.uuid4())
    answer = generate_response(request.message, session_id)
    return {"answer": answer, "session_id": session_id}
    
@app.get("/ask_no_userID")
def ask(question: str):
    return {"answer": generate_response(question, session_id="global")}

@app.get("/ask_no_memory")
def ask(question: str):
    return {"answer": generate_response_no_memory(question)}

@app.get("/")
def read_root():
    return {"message": "Uniche API works!"}

def gradio_wrapper(message, history):
    """
    Wrapper function to connect Gradio to LLM.
    Gradio passes 'message' (current text) and 'history' (past chat).
    Use a fixed session_id for the UI to keep it simple.
    """
    # Use a specific ID for the web UI user so they have their own memory space
    return generate_response(message, session_id="gradio-web-ui")

# Create the Chat Interface
demo = gr.ChatInterface(
    fn=gradio_wrapper,  # (in general) function that governs the response of the chatbot based on the user input and chat history. 
    title="UNICHE Chat",
    description="Ask me anything!"
)

# Mount gradio app to fastAPI at /ui
app = gr.mount_gradio_app(app, demo, path="/ui")