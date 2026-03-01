import joblib

model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def predict(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]