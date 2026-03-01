# rating-evaluation

# MLOps Sentiment Analysis Project

## Overview

Sentiment classification model using TF-IDF + Logistic Regression.

## Features

-   MLflow experiment tracking
-   Model Registry versioning
-   REST API serving
-   Docker-ready architecture

## Run Training

``` bash
python -m src.train
```

## Serve Model

``` bash
mlflow models serve -m "models:/SentimentModel/1" -p 8000 --env-manager=local
```

## Future Improvements

- Postgres backend
- Kafka streaming ingestion
- Cloud deployment

# structure
project/
│
├── src/
│   ├── train.py
│   ├── predict.py
│   ├── preprocessing.py
│   ├── model.py
│
├── app/
│   └── main.py
│
├── models/
├── data/
├── requirements.txt
└── Dockerfile

# src/preprocessing.py
Limpeza de texto
Construção do TF-IDF
Função de transformação

# src/model.py
Construção do modelo
Retornar modelo configurado

# src/train.py
Carregar dados
Treinar modelo
Avaliar
Salvar artefatos

# src/predict.py
Carregar modelo salvo
Fazer previsão em texto novo

# app/main.py
Criar API
Expor endpoint de previsão
 
#  Comando para iniciar localmente
mlflow server -> inicia server do mlflow local
source .venv/bin/activate -> inicia dependencias rating-evaluation
necessidade de adicionar nova lib py? -> uv add (nome lib). uv é um composer de PY

# Feito
Dataset
Pipeline de treino
Vectorizer
Modelo
MLflow Tracking
MLflow Registry
Versionamento automático

mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 127.0.0.1 \
  --port 5000