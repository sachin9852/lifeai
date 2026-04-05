from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Enable CORS so your Netlify frontend can talk to this Vercel backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure AI
genai.configure(api_key="AIzaSyCyIQy22wuUH5EFRaUZmMp3ERDKVg5e2lM")

class AIRequest(BaseModel):
    goal: str
    personality: str

@app.post("/api/generate")
async def generate_plan(req: AIRequest):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Context: You are 'LifeAI', a productivity coach.
        User Goal: {req.goal}
        Persona Style: {req.personality}
        
        Task: Create a high-energy, 4-hour time-blocked schedule.
        Format: Use clean bullet points with times. No large markdown headers.
        """
        
        response = model.generate_content(prompt)
        return {"status": "success", "schedule": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
