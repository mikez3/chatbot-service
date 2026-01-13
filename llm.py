from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
# import ollama

model = "ministral-3:3b"
# model = "smollm:135m"

# Initialiation
llm = ChatOllama(model=model)

# Prompt tmeplate
prompt = ChatPromptTemplate.from_messages([
    # System prompt:
    ("system", "You are the UNICHE Cultural Heritage Guide, an advanced AI agent integrated into the UNICHE platform. "
     "Your goal is to enhance visitor engagement at cultural heritage sites (museums, archaeological sites, and virtual exhibitions) by providing highly relevant, accurate, and personalized assistance." 
     "Your answers must be max 2 sentences."),
    MessagesPlaceholder("history"),   # <- Past conversation history
    ("human", "{input}"),   # <- Current user message
])

# Create the chain with the prompt
runnable = prompt | llm     # | = pipe = LangChain Expression Language, python: "response = llm(prompt(input))"


# Simple in-memory storage for conversation history -> dictionary
store = {}
# Looks like: { "session_123": [Message1, Message2], "session_456": [...] }

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()    # Create empty history
    return store[session_id]

# Create the conversational chain - Chain + Memory -> Wraps everything together
# Save to list -> Read from list -> Insert into prompt
chain = RunnableWithMessageHistory(
    runnable,                           # prompt | llm
    get_session_history,                # Function to get/create history
    input_messages_key="input",         # Where to find user's message
    history_messages_key="history",     # Where to find past messages
)

def generate_response(message: str, session_id: str = "default") -> str:
    response = chain.invoke(
        {"input": message}, # User's message
        config={"configurable": {"session_id": session_id}},    # Which history to use
    )
    return response.content
        # model=model,
        # messages=[
        #     # {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": message}
        # ],
        # options={
        # "num_predict":8,
        # "temperature":0.7,
        # "top_p":0.9,
        # "frequency_penalty":0,
        # "presence_penalty":0
        # },
    # )
    # answer = response.message.content
    # return answer
# Add this new function for stateless calls
def generate_response_no_memory(message: str) -> str:
    response = runnable.invoke({"input": message, "history": []})
    return response.content