import mlflow
import mlflow.sklearn
import pandas as pd
import joblib

from sklearn import pipeline
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from preprocessing import build_vectorizer
from model import build_model
import os

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
# os.environ["AWS_DEFAULT_REGION"] = "my_region"


def train():

    # Configurar MLflow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("Sentiment-Analysis")

    # Carregar dados
    df = pd.read_sql_table("reviews", "postgresql://dev_user:1234@localhost:5432/reviews_dev")

    df["sentiment"] = df["type"].map({
        "Positive": 1,
        "Negative": 0
    })

    X = df["review"]
    y = df["sentiment"]

    # Split com stratify
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Vetorização
    vectorizer = build_vectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Modelo
    model = build_model()

    with mlflow.start_run():

        model.fit(X_train_vec, y_train)

        y_pred = model.predict(X_test_vec)
        f1 = f1_score(y_test, y_pred)

        print(classification_report(y_test, y_pred))

        pipeline = Pipeline([
        ("tfidf", vectorizer),
        ("clf", model)
    ])

        pipeline.predict(X_train)

        # Logar parâmetros e métricas
        mlflow.log_param("model_type", "logistic_regression")
        mlflow.log_param("vectorizer", "tfidf")
        mlflow.log_metric("f1_score", f1)

        # Registrar modelo no Model Registry
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="model",
            registered_model_name="SentimentModel"
        )

    # # Salvar localmente também
    # joblib.dump(model, "models/model.pkl")
    # joblib.dump(vectorizer, "models/vectorizer.pkl")

    print("Treinamento finalizado.")


if __name__ == "__main__":
    train()