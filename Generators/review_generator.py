from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.agents import create_agent
from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from kafka import KafkaProducer, KafkaConsumer
from kafka.structs import TopicPartition
from queue import Queue
import json
from DataHandlers.loaders.kafka.kafka_publisher import kafka_publisher
from Agents.review_generator_agent import generate_review
pd.options.display.max_columns = None

models = [ 
            "gemma3:1b", 
            "deepseek-r1:1.5b",
            "qwen3:1.7b", 
            "granite3.3:2b", 
            "llama3.2:1b",
        ]

fila = Queue(100)

df = pd.read_csv('data/produtcs.csv')
products = df.values

with ThreadPoolExecutor(max_workers=len(models)) as executor:
	while True:
		futures = [executor.submit(generate_review, model, products) for model in models]
		for future in as_completed(futures):
			review = future.result()
			
			if review:
				fila.put(review)

			if fila.full():
				print("Fila cheia, aguardando consumo...")
				while not fila.empty():
					review = fila.get()
					kafka_publisher(topic="reviews", message=review)
				print("Fila vazia, continuando processamento...")
