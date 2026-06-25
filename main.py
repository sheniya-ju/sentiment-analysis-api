from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from transformers import pipeline
from database import save_prediction, get_all_predictions
from rag import add_document, answer_question

app = FastAPI()

# Load sentiment model once at startup
classifier = pipeline("sentiment-analysis")

# Input models
class TextInput(BaseModel):
    text: str

class QuestionInput(BaseModel):
    question: str

# Existing endpoints
@app.get("/")
def home():
    return {"message": "Sentiment Analysis + RAG API is running!"}

@app.post("/predict")
def predict(input: TextInput):
    result = classifier(input.text)[0]
    sentiment = result["label"]
    confidence = round(result["score"], 4)
    save_prediction(input.text, sentiment, confidence)
    return {
        "text": input.text,
        "sentiment": sentiment,
        "confidence": confidence
    }

@app.get("/history")
def history():
    return get_all_predictions()

# New RAG endpoints
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    chunks_added = add_document(file.filename, text)
    return {
        "filename": file.filename,
        "chunks_stored": chunks_added,
        "message": f"Document uploaded and split into {chunks_added} chunks in ChromaDB"
    }

@app.post("/ask")
def ask(input: QuestionInput):
    answer = answer_question(input.question)
    return {
        "question": input.question,
        "answer": answer
    }