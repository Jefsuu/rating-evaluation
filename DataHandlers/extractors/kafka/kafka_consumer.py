from confluent_kafka import Consumer, KafkaException
import json

# conf = {
# 		'bootstrap.servers': 'localhost:9092',
# 		'group.id': 'review-group',
# 		'auto.offset.reset': 'earliest',  # earliest | latest
# 		'enable.auto.commit': False
# 	}

def kafka_consumer(conf, topic: str,):

	consumer = Consumer(conf)

	consumer.subscribe([topic])
	empty_polls = 0
	max_empty_polls = 5  # para após 5 tentativas sem mensagem

	try:
		json_records = []
		records = consumer.consume(timeout=1.0, num_messages=100)

		if records is None:
			empty_polls += 1
			print(f"Sem mensagens... ({empty_polls})")

			if empty_polls >= max_empty_polls:
				print("Não há mais mensagens. Encerrando.")
				return []
		
		for msg in records:
			if msg.error():
				raise KafkaException(msg.error())
			else:

				# Caso a mensagem esteja em JSON
				try:
					value = json.loads(msg.value().decode('utf-8'))
				except Exception:
					value = msg.value().decode('utf-8')

				json_records.append(value)
				consumer.commit(msg)

		return json_records

	finally:
		consumer.close()
		print("Consumer encerrado com sucesso.")