# src/data_generator.py

import pandas as pd
import numpy as np
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Review(BaseModel):
    review: str = Field(description="Text of the review")
    stars: int = Field(description="The quantity of stars on the rating")


def build_llm():
    return OllamaLLM(
        model="gemma3:12b",
        temperature=0.5,
        seed=1234
    )


def generate_reviews(qt_reviews=1000):

    llm = build_llm()
    parser = PydanticOutputParser(pydantic_object=Review)

    prompt = ChatPromptTemplate(
        (["system", "... seu prompt aqui ..."]),
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    chain = prompt | llm | parser

    df = pd.read_csv("data/products.csv")
    products = df.values

    list_of_reviews = []

    for i in range(qt_reviews):

        product = products[np.random.randint(len(products))]

        output = chain.invoke({
            "product_name": product[0],
            "product_category": product[1],
            "review_size": "Medium",
            "type": np.random.choice(["Positive", "Negative"]),
            "content": "Delivery"
        })

        data = {
            "review_text": output.review,
            "sentiment": 1 if output.stars >= 4 else 0,
            "stars": output.stars
        }

        list_of_reviews.append(data)

    pd.DataFrame(list_of_reviews).to_csv("data/reviews_generated.csv", index=False)