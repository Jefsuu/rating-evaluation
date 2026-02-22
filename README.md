# rating-evaluation

# structure
# project/
# │
# ├── src/
# │   ├── train.py
# │   ├── predict.py
# │   ├── preprocessing.py
# │   ├── model.py
# │
# ├── app/
# │   └── main.py
# │
# ├── models/
# ├── data/
# ├── requirements.txt
# └── Dockerfile



# src/preprocessing.py
# Limpeza de texto
# Construção do TF-IDF
# Função de transformação
# 
# src/model.py
# Construção do modelo
# Retornar modelo configurado
# 
# src/train.py
# Carregar dados
# Treinar modelo
# Avaliar
# Salvar artefatos
# 
# src/predict.py
# Carregar modelo salvo
# Fazer previsão em texto novo
# 
# app/main.py
# Criar API
# Expor endpoint de previsão


# Revisar para docker
# python -m pip install joblib scikit-learn pandas fastapi uvicorn mlflow
#
# Arquitetura atualizada
# Notebook / train.py
#         ↓
#  MLflow Tracking
#         ↓
#  MLflow Model Registry
#         ↓
#  Registered Model (v1, v2, v3...)
#         ↓
#  FastAPI carrega versão Production
# 
# 
# 
# 
