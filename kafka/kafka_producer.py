import json

from data_producer import DataProducer
from confluent_kafka import Producer


class KafkaProducer(DataProducer):
    """
    This class implements the abstract class DataProducer to produce data on Kafka

    It contains two methods: delivery_report and the concrete method produce

    """
    producer = Producer({'bootstrap.servers': 'kafka:9092'})

    def delivery_report(self, err, msg):
        """

        This method makes a report for the producer to make sure that
        the data is produced to the right topic.

        Parameters:
            err (dict): specifies the error of the production.
            msg (kafka object): Specifies the message produced.

        """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce(self, data: dict):
        """

        This method overrides the abstract method to produce the data to Kafka.

        Parameters:
            data (dict): A dictionary containing the data to be published.

        """
        final_data = json.dumps(data)
        self.producer.produce('kafka_simulated_data', key="key", value=final_data,
                         callback=self.delivery_report)
        self.producer.flush()
