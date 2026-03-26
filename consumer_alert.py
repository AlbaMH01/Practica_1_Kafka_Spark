from kafka import KafkaConsumer
import json
from config import TOPIC_FATIGA

def create_consumer(topic_name) -> KafkaConsumer:
    return KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def leer_datos(consumer):
    try:
        print("Looking for alerts......")
        for message in consumer:
            data = message.value
            bpm = data.get('bpm')
            speed = data.get('speed_kmh')
        
            if bpm is not None and speed is not None and bpm > 180 and speed < 10:
                print(40 * "-")
                print(f"🚨 ALERTA: El jugador {data.get('player_id')} tiene {bpm} BPM a solo {speed} km/h.")
                print(40 * "-")

    except KeyboardInterrupt:
        print("Consumer manually interrupted")
    finally:
        consumer.close()

if __name__ == '__main__':
    consumer = create_consumer(TOPIC_FATIGA)
    leer_datos(consumer)