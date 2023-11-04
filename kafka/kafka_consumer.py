import pandas as pd
import os

from confluent_kafka import Consumer
import threading
import json

consumer_thread = None


def consume(topic):
    """
    This method starts the polling thread of the consumer

    Parameters:
        topic (str): The topic that the consumer will subscribe to.

    """
    global consumer_thread

    c = Consumer({'bootstrap.servers': 'kafka:9092', 'group.id': 'g1', 'auto.offset.reset': 'latest'})

    def poll():
        """
        This method polls the data from the broker in background

        """
        print(f"consuming data from {topic}", flush=True)
        c.subscribe([topic])

        while True:
            msg = c.poll()
            if msg is None:
                print("No messages yet", flush=True)
                continue
            if msg.error():
                print("consumer error: {}".format(msg.error()), flush=True)
                continue

            data_df = pd.DataFrame(json.loads(msg.value()), index=[0])
            os.makedirs("./kafka_datasets", exist_ok=True)
            data_df.to_csv(f"./kafka_datasets/{msg.timestamp()[1]}.csv", encoding='utf-8', index=False)

    if consumer_thread is None:
        consumer_thread = threading.Thread(target=poll)
        consumer_thread.daemon = True
        consumer_thread.start()
