from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.agents import create_agent
from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
# from langchain.agents.structured_output import 
import pandas as pd
import numpy as np
pd.options.display.max_columns = None


class Product(BaseModel):
    name: str = Field(
        description="Name of the product"
    )
    category: str = Field(
        description="Category of the product"
    )


class ProductList(BaseModel):
    products: List[Product]

parser = PydanticOutputParser(pydantic_object=ProductList)

str_prompt = """
Role:
- You are a product generator agent.

Objective:
- Generate a list of products based on the requested quantity.

Input Parameter:
- quantity (integer): the number of products to generate.

Quantity to generate: {quantity}

Rules:

- Only generate products that belong to one of the following categories:
   - Appliances
   - Furniture
   Examples of valid products include (but are not limited to):

   - Appliances: refrigerator, air conditioner, stove, washing machine, microwave
   - Furniture: sofa, wardrobe, bed, table, chair

- The product name must strictly follow this pattern:

   [BRAND] [MODEL]

   Example: Samsung RT38
   Example: Ikea KLIPPAN

- Each generated product must include:

   name (string): following the required naming pattern

   category (string): Must be the type of the product. 
   Ex: refrigerator, sofa, air conditioner, etc.

- Brands can be real brands.

- Name and category must be generated in upper case.

{format_instructions}
"""

prompt = ChatPromptTemplate(
      (["system", str_prompt]),
      partial_variables={"format_instructions": parser.get_format_instructions()}
      )

def generate_products(model, quantity: int):
    llm = OllamaLLM(
        model=model,
        temperature=0.8,
        validate_model_on_init=True,
        seed=1234,
        num_ctx=32768,
        reasoning=False
        
    )
    chain = prompt | llm | parser
    output = chain.invoke({"quantity": quantity})
    
    return output