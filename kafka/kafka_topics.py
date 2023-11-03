from confluent_kafka.admin import AdminClient, NewTopic


def create_topic(topic_name):
    ac = AdminClient({'bootstrap.servers': 'kafka:9092'})
    topic_metadata = ac.list_topics(timeout=10)

    if not (topic_name in topic_metadata.topics):
        topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)

        ac.create_topics([topic])
    else:
        print('Topic already exists')
