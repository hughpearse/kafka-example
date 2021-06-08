from kafka import KafkaConsumer, KafkaProducer
import json
import os

kafka_hostname = os.environ['KAFKA_SERVER']
consumer = KafkaConsumer('drinkorders', value_deserializer=lambda x: json.loads(x.decode('utf-8')), bootstrap_servers=kafka_hostname, api_version=(2,8,0), auto_offset_reset='earliest', enable_auto_commit=True, group_id='bartender_drinkorders')
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=kafka_hostname, api_version=(2,8,0))

for message in consumer:
    drink = message.value["drink"]
    data = {drink : "READY"}
    producer.send('servicewindow', value=data)
    producer.flush()
