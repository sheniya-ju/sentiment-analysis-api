# Sentiment Analysis API

A REST API that classifies text as POSITIVE or NEGATIVE using a pre-trained Hugging Face NLP model, built with FastAPI and MySQL.

## Tech Stack
- Python
- FastAPI
- Hugging Face Transformers (DistilBERT)
- MySQL
- Uvicorn

## Endpoints
- `GET /` — Health check
- `POST /predict` — Analyse sentiment of input text
- `GET /history` — Retrieve all past predictions from database

## How to Run
1. Install dependencies: `pip install fastapi uvicorn transformers torch mysql-connector-python`
2. Set up MySQL database and update password in `database.py`
3. Run: `uvicorn main:app --reload`
4. Open: `http://127.0.0.1:8000/docs`

## Example
Input:
{"text": "I love building AI projects!"}

Output:
{"text": "I love building AI projects!", "sentiment": "POSITIVE", "confidence": 0.999}
