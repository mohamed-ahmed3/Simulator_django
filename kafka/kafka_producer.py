import json

from data_producer import DataProducer
from confluent_kafka import Producer


class KafkaProducer(DataProducer):
    producer = Producer({'bootstrap.servers': 'kafka:9092'})

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce(self, data: dict):
        # create_topic(topic_name)
        final_data = json.dumps(data)
        self.producer.produce('simulated_data', key="key", value=final_data,
                         callback=self.delivery_report)
        self.producer.flush()
