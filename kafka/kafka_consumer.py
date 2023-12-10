import dataclasses

import pandas as pd
import os

from confluent_kafka import Consumer
import threading
import json

from jsonschema import validate


class Validator:
    schema = {
        "type": "object",
        "properties": {
            "attribute_id": {"type": "string"},
            "value": {"type": "number"},
            "timestamp": {"type": "string"},
            "asset_id": {"type": "string"},
        },
    }


class KafkaConsumer:
    consumer_thread = None

    def __init__(self, topic):
        self.topic = topic

    def consume(self):
        """
        This method starts the polling thread of the consumer

        """
        if KafkaConsumer.consumer_thread is not None:
            print("Consumer thread is already running.")
            return

        c = Consumer({'bootstrap.servers': 'kafka:9092', 'group.id': 'g1', 'auto.offset.reset': 'latest'})

        def poll():
            """
            This method polls the data from the broker in background

            """
            print(f"consuming data from {self.topic}", flush=True)
            c.subscribe([self.topic])

            while True:
                msg = c.poll()
                validator = Validator
                schema = validator.schema

                data_str = msg.value().decode('utf-8')
                data_dict = json.loads(data_str)

                try:
                    validate(instance=data_dict, schema=schema)
                    if msg is None:
                        print("No messages yet", flush=True)
                        continue
                    if msg.error():
                        print("consumer error: {}".format(msg.error()), flush=True)
                        continue

                    data_df = pd.DataFrame(data_dict, index=[0])
                    os.makedirs("./kafka_datasets", exist_ok=True)
                    data_df.to_csv(f"./kafka_datasets/{msg.timestamp()[1]}.csv", encoding='utf-8', index=False)

                except Exception as e:
                    print(str(e))

        KafkaConsumer.consumer_thread = threading.Thread(target=poll)
        KafkaConsumer.consumer_thread.daemon = True
        KafkaConsumer.consumer_thread.start()
