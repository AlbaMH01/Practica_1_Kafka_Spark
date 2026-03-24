from kafka import KafkaConsumer
import json
from config import TOPIC_FATIGA

def create_consumer(topic_name) -> KafkaConsumer:
    """Create and return a KafkaConsumer instance.

    Configured to connect to the local broker (localhost:9092)
    and read from the beginning of the topic.

    Returns:
        KafkaConsumer
    """
    return KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset = 'earliest', # Lee todo desde el comienzo
        value_deserializer = lambda x: json.loads(x.decode('utf-8'))
    )


def leer_datos(consumer):
    """
    Bucle infinito para leer los mensajes entrantes de Kafka.
    """
    try:
        print("Escuchando mensajes... (Pulsa Crtl+C para parar)")
        for mensaje in consumer:
            datos = mensaje.value
            print(f"Recibido: {datos}")

    except KeyboardInterrupt:
        print("Consumidor detenido manualmente")
    finally:
        consumer.close()


if __name__ == "__main__":
    consumer = create_consumer(TOPIC_FATIGA)
    leer_datos(consumer)