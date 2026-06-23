from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from database import save_prediction, get_all_predictions

app = FastAPI()

# Load the Hugging Face sentiment model once at startup
classifier = pipeline("sentiment-analysis")

# Define the input structure
class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is running!"}

@app.post("/predict")
def predict(input: TextInput):
    result = classifier(input.text)[0]
    sentiment = result["label"]
    confidence = round(result["score"], 4)

    # Save to MySQL
    save_prediction(input.text, sentiment, confidence)

    return {
        "text": input.text,
        "sentiment": sentiment,
        "confidence": confidence
    }

@app.get("/history")
def history():
    return get_all_predictions()