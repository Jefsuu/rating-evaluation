from fastapi import FastAPI
from src.predict import predict

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Sentiment Model API"}


@app.post("/predict")
def get_prediction(review: str):
    result = predict(review)
    return {"prediction": result}