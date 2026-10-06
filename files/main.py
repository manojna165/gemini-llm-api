import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

app = FastAPI(title="Gemini LLM API")


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)


@app.get("/")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/generate")
def generate(req: PromptRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured")

    payload = {"contents": [{"parts": [{"text": req.prompt}]}]}
    headers = {"Content-Type": "application/json", "x-goog-api-key": API_KEY}

    try:
        resp = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=300)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Gemini API request timed out")
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Could not reach Gemini API: {exc}")

    if resp.status_code != 200:
        try:
            message = resp.json().get("error", {}).get("message", resp.text)
        except ValueError:
            message = resp.text
        if resp.status_code in (400, 401, 403):
            raise HTTPException(status_code=resp.status_code, detail=f"Gemini rejected the request: {message}")
        if resp.status_code == 429:
            raise HTTPException(status_code=429, detail="Rate limit or quota exceeded")
        raise HTTPException(status_code=502, detail=f"Gemini API error: {message}")

    try:
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise HTTPException(status_code=502, detail="Empty or blocked response from Gemini")

    return {"model": MODEL, "prompt": req.prompt, "response": text}
