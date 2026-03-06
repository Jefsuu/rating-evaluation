import pandas as pd
import requests
from sqlalchemy import create_engine


engine = create_engine("postgresql://dev_user:1234@postgresql:5432/reviews")
df_max_id = pd.read_sql_query("SELECT coalesce(max(review_id), 0) max_id FROM rated_reviews", con=engine)
max_id = int(df_max_id.iloc[0, 0])
df_reviews = pd.read_sql_query(f"SELECT * FROM reviews WHERE id > {max_id} ORDER BY id ASC LIMIT 1", con=engine)

session = requests.Session()

def evaluator_caller(review):
    data = {
		"dataframe_split": {
			"columns": ["review"],
			"data": [review]
		}
	}
    response = session.post(
		"http://model-server:5001/invocations",
		json=data,
        verify=False,
        timeout=60
		# headers={"Content-Type": "application/json"}
	)
    return response.json()['predictions'][0]


df_reviews['is_positive'] = df_reviews['review'].apply(evaluator_caller)
df_reviews.rename(columns={'id': 'review_id'}, inplace=True)
df_reviews['is_positive'] = df_reviews['is_positive'].apply(lambda x: True if x == 1 else False)
df_reviews[['review_id', 'is_positive']].to_sql('rated_reviews', con=engine, if_exists='append', index=False)