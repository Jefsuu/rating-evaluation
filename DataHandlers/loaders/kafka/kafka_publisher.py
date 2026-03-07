
from typing import List
from kafka import KafkaProducer
import json

def kafka_publisher(topic: str, message: dict, bootstrap_servers: List[str] = ["localhost:29092"]):
    """
    Publish a message to a Kafka topic.
    
    Args:
        topic (str): The Kafka topic to publish to
        message (dict): The message to publish (will be converted to JSON)
        bootstrap_servers (str): Kafka broker address(es), defaults to "localhost:9092"
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3,
            api_version=(4, 2, 0)
        )
        producer.send(topic, value=message)
        producer.flush()
        
        # print(f"Message published to topic '{topic}' at partition {record_metadata.partition}, offset {record_metadata.offset}")
        return True
    except Exception as e:
        print(f"Error publishing to Kafka: {e}")
        return False
