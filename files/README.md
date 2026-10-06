# Gemini LLM API (FastAPI)

A simple FastAPI service that takes a user prompt, sends it to the Google Gemini API, and returns the response.

## Features
- `POST /generate` endpoint for sending a prompt and receiving an LLM response
- API key stored in an environment variable (`.env`, not committed)
- Error handling for missing key, invalid input, timeouts, rate limits, and upstream API errors
- Tested with Swagger UI (`/docs`)

## Setup
```
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` and add your key from https://aistudio.google.com/apikey:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```
Run:
```
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs

## Usage
`POST /generate`
```json
{"prompt": "explain ai in one line"}
```
Response:
```json
{
  "model": "gemini-3.8-flash",
  "prompt": "explain ai in one line",
  "response": "AI is technology that enables machines to learn, solve problems, and perform tasks that typically require human intelligence."
}
```

## Test Results

| # | Test | Status | Result | Screenshot |
|---|------|--------|--------|------------|
| 1 | Valid prompt | 200 | Response returned from Gemini | screenshots/01_success.png |
| 2 | Empty prompt | 422 | Validation error | screenshots/02_validation.png |
| 3 | API key not set | 500 | `GEMINI_API_KEY is not configured` | screenshots/03_missing_key.png |
| 4 | Project denied access | 403 | `Gemini rejected the request` | screenshots/04_denied.png |
| 5 | Model overloaded | 502 | `Gemini API error` | screenshots/05_upstream_error.png |
| 6 | Request timed out | 504 | `Gemini API request timed out` | screenshots/06_timeout.png |

## Error Handling

| Case | Status |
|------|--------|
| Missing or invalid input | 422 |
| API key not configured | 500 |
| Gemini rejects key or project | 400 / 401 / 403 |
| Rate limit or quota exceeded | 429 |
| Gemini unreachable or returns an error | 502 |
| Request timeout | 504 |
