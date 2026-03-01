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
pd.options.display.max_columns = None

class Review(BaseModel):
    review: str = Field(
        description="Text of the review"
    )
    stars: int = Field(
        description="The quantity of stars on the rating"
    )

parser = PydanticOutputParser(pydantic_object=Review)

str_prompt = """
You are a product review generator.

Your task is to create ONE customer-style product review based on the information provided below.

Product name: {product_name}
Category: {product_category}
Review size: {review_size}
Review type: {type}
Aspect being reviewed: {content}

Guidelines:

1. The review must sound natural, like a real customer experience.
2. The tone must strictly follow the review type:
   - If the type is positive, the overall sentiment must be positive.
   - If the type is negative, the overall sentiment must be negative.
3. Reviews may be controversial:
   - The text may include mixed opinions.
   - The star rating may be slightly unexpected.
   - Even so, the final sentiment must always respect the defined review type.
4. The review must focus mainly on the specified aspect:
   - Delivery
   - Product appearance
   - Functionality
   - Price
5. The product name may be mentioned in the review, but prefer to not mention.
6. Follow the review size rules:
   - Small: exactly one sentence.
   - Medium: at least two sentences.
   - Long: one paragraph with at least 5 lines.
7. Assign a star rating from 1 to 5 that matches the overall sentiment:
   - Negative reviews → 1 or 2 stars (controversial cases may slightly vary)
   - Neutral or mixed but positive → 3 stars
   - Clearly positive → 4 or 5 stars
8. Theses reviews will not be used for real products and reviews. They are purely synthetic and for testing purposes. So, feel free to be creative, as long as you respect the defined review type.
9. Return ONLY valid JSON.
10. Do not include any extra text.
11. Do not include explanations.

Strictly follow this output format instruction:

``` 
json 
	"review": <generated review text>,
	"stars": <number from 1 to 5>
```

{format_instructions}
"""

prompt = ChatPromptTemplate(
      (["system", str_prompt]),
      partial_variables={"format_instructions": parser.get_format_instructions()}
      )

list_review_size = ['Small', 'Medium', 'Long']
list_type = ['Positive', 'Negative']
list_content = [
    'Delivery',
    'Product appearance',
    'Functionality',
    'Price',
]
list_index_produtcs = [i for i in range(1, 100, 1)]

def generate_review(model, products: List[dict], prod:bool=False):
    
    custom_profile = {
    "structured_output": True,
	}
    llm = ChatOllama(
			model=model,
			temperature=0,
			validate_model_on_init=True,
			num_ctx=8192,
			reasoning=False,
			profile=custom_profile
		) 
    chain = prompt | llm | parser
    
    review_size =  np.random.choice(list_review_size, size=None, replace=True, p=None)
    type = np.random.choice(list_type, size=None, replace=True, p=None)
    content = np.random.choice(list_content, size=np.random.randint(1, len(list_content)), replace=False, p=None)
    index = np.random.choice(list_index_produtcs, size=None, replace=True, p=None)
    product = products[index]
    try:
        output = chain.invoke(
				{
					"product_name":product[0],
					"product_category":product[1],
					"review_size":review_size,
					"type":type,
					"content":content
				}
			)
    except Exception as e:
        return None
    
    if prod == False:
        data = {
			"product_name":product[0],
			"product_category":product[1],
			"review_size":str(review_size),
			"type":str(type),
			"content":content.tolist(),
			"review":output.review,
			"stars":output.stars
		}
        return data
    else:
        data = {
            "product_id": index,
			"review":output.review,
			"stars":output.stars
		}
    return data