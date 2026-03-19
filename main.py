from fastapi import FastAPI
from pydantic import BaseModel
from mcp_server import search_wikipedia
from groq import Groq
import os, uvicorn

app = FastAPI(title="MCP Wiki Agent")

# Hardcode key directly for now
GROQ_API_KEY = "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"  # ← paste your gsk_... key here
client = Groq(api_key=GROQ_API_KEY)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def health():
    return {"status": "ok", "agent": "mcp-wiki-agent"}

@app.post("/ask")
async def ask(request: QueryRequest):
    wiki_data = search_wikipedia(request.query)
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful research assistant. Summarize the Wikipedia data clearly and mention it came from Wikipedia."
            },
            {
                "role": "user",
                "content": f"User asked: {request.query}\n\nWikipedia data: {wiki_data}"
            }
        ]
    )
    
    return {
        "query": request.query,
        "response": response.choices[0].message.content,
        "source": "Wikipedia via MCP + Groq LLM"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))