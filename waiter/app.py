from flask import Flask, request
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
import os

app = Flask(__name__)
kafka_hostname = os.environ['KAFKA_SERVER']
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=kafka_hostname, api_version=(2,8,0))
consumer = KafkaConsumer('servicewindow', consumer_timeout_ms=500, bootstrap_servers=kafka_hostname, api_version=(2,8,0), value_deserializer=lambda x: json.loads(x.decode('utf-8')), auto_offset_reset='earliest', enable_auto_commit=True, group_id='waiter_servicewindow')

@app.route('/order', methods=['POST'])
def order_drink():
    drink = request.get_json()["name"]
    data = {"drink" : drink}
    producer.send('drinkorders', value=data)
    producer.flush()
    return "Success\n"

@app.route('/collect', methods=['GET'])
def collect_drinks():
    items = {"drinks" : []}
    for message in consumer:
        print("processing: " + str(message))
        items["drinks"].append(message.value)
    return items

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))
