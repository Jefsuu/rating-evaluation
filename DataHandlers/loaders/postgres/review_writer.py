import psycopg2
from psycopg2.extras import execute_values

def write_batch_to_postgres(records: list, table: str, conn_params: dict):
    """Write a list of JSON-serializable records to Postgres in a specified table.

    If the table does not exist, it will be created with a simple schema
    (`id SERIAL PRIMARY KEY, data JSONB`). Records are inserted as JSONB.
    """
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id SERIAL PRIMARY KEY,
            product_id int,
			--product_category varchar,
			--review_size varchar,
			--type varchar,
			--content TEXT[],
			review varchar,
			stars int
        )
        """
    )
    conn.commit()

    if records:
        execute_values(
            cur,
            # f"INSERT INTO {table} (product_name, product_category, review_size, type, content, review, stars) VALUES %s",
            f"INSERT INTO {table} (product_id, review, stars) VALUES %s",
            [
				(
					# rec.get("product_name", ""),
					# rec.get("product_category", ""),
					# rec.get("review_size", ""), 
					# rec.get("type", ""), 
					# rec.get("content", []), 
					# rec.get("review", ""), 
					# rec.get("stars", 0)
                    rec.get("product_id", 0),
					rec.get("review", ""), 
					rec.get("stars", 0)
				) 
				for rec in records
			],
        )
        conn.commit()
    cur.close()
    conn.close()