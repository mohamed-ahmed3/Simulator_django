from kafka.kafka_producer import KafkaProducer
from data_producer import *


class DataProducerFileCreation:

    @classmethod
    def create(cls, sink: str):
        """
        Factory method to create a specific DataProducer instance based on the sink type.

        Parameters:
            sink (str): The destination where data will be produced.

        Returns:
            DataProducer: An instance of a DataProducer subclass (e.g., CsvDataProducer).

        Raises:
            ValueError: If the sink type is not supported.
        """
        if sink.endswith("csv"):
            return CsvDataProducer(sink)
        elif sink.endswith("Kafka"):
            return KafkaProducer(sink)
        else:
            raise ValueError(f"Unsupported sink: {sink}")



