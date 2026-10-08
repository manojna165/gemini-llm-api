import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from prompts import ZERO_SHOT_PROMPT, IMPROVED_ZERO_SHOT_PROMPT, FEW_SHOT_PROMPT
from schemas import SentimentResponse

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

app = FastAPI(title="Gemini LLM API - Prompt Engineering")


# Request models
class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)

class ReviewRequest(BaseModel):
    review: str = Field(..., min_length=1, max_length=4000)


# Task 2 - Health check
@app.get("/")
def health():
    return {"status": "ok", "model": MODEL}


# Task 2 - Basic Gemini API
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


# Task 3 - Generate and validate structured JSON
def generate_structured_response(prompt: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": SentimentResponse.model_json_schema()
        }
    }
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
        raise HTTPException(status_code=502, detail="Empty or invalid response from Gemini")

    # Validate Gemini's JSON response using Pydantic
    try:
        return SentimentResponse.model_validate_json(text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Invalid structured output: {exc}")

# Task 3 - Basic zero-shot
@app.post("/zero-shot")
def zero_shot(req: ReviewRequest):
    prompt = ZERO_SHOT_PROMPT.format(review=req.review)
    result = generate_structured_response(prompt)
    return {"prompt_type": "Zero-Shot", "result": result.model_dump()}


# Task 3 - Improved zero-shot
@app.post("/improved-zero-shot")
def improved_zero_shot(req: ReviewRequest):
    prompt = IMPROVED_ZERO_SHOT_PROMPT.format(review=req.review)
    result = generate_structured_response(prompt)
    return {"prompt_type": "Improved Zero-Shot", "result": result.model_dump()}


# Task 3 - Few-shot
@app.post("/few-shot")
def few_shot(req: ReviewRequest):
    prompt = FEW_SHOT_PROMPT.format(review=req.review)
    result = generate_structured_response(prompt)
    return {"prompt_type": "Few-Shot", "result": result.model_dump()}
   
