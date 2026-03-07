from DataHandlers.loaders.postgres.review_writer import write_batch_to_postgres
from DataHandlers.extractors.kafka.kafka_consumer import kafka_consumer
from typing import List

def kafka_to_postgres(
    conn_params: dict,
    table: str = "reviews",
    batch_size:int = 100,
    kafka_conf: dict = None,
    topic: str = "reviews"
):
    """Consume messages from Kafka in micro‑batches and load them into Postgres.

    The function repeatedly reads up to `batch_size` messages using
    ``kafka_consumer`` and writes each batch to the specified Postgres table
    until there are no more available messages. ``conn_params`` should be a
    dict suitable for ``psycopg2.connect`` (e.g. ``{
    "host":...,"port":...,"user":...,"password":...,"dbname":...}``).
    """
    while True:
        batch = kafka_consumer(kafka_conf, topic)
        if not batch:
            print("no new messages available, stopping consumer")
            break
        write_batch_to_postgres(batch, table, conn_params)
        print(f"inserted microbatch of {len(batch)} records into {table}")


# example usage
conn_params = {
    "host": "postgresql",
    "port": 5432,
    "user": "dev_user",
    "password": "1234",
    # the default postgres database is 'postgres'; set to your target DB if different
    "dbname": "reviews",
}

conf = {
		'bootstrap.servers': 'kafka:9092',
		'group.id': 'review-group',
		'auto.offset.reset': 'earliest',  # earliest | latest
		'enable.auto.commit': False
	}

# consume all available reviews in microbatch sizes of 100 and load into Postgres
default_batch = 100
kafka_to_postgres(conn_params, table="reviews", batch_size=default_batch, kafka_conf=conf, topic="reviews")