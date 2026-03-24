---
title: "Práctica 1: Streaming de Datos Deportivos con Apache Kafka"
author: "Alba Martínez de la Hermosa y Alonso González Romero"
format: 
  html:
    theme: cosmo
    toc: true
    toc-title: "Índice"
---

## 1. Introducción
Esta memoria detalla la implementación de un sistema de procesamiento de datos en tiempo real (streaming) basado en Apache Kafka. El sistema simula la ingesta y consumo de datos telemétricos de jugadores de fútbol durante un partido, procesando métricas como posición, velocidad, aceleración y frecuencia cardíaca.

---

## 2. Diseño de la Arquitectura de Datos

### 2.1. Diseño del Topic

Para la publicación de los eventos, se ha establecido una convención de nomenclatura jerárquica que permite escalar el sistema en el futuro. 

* **Nombre del Tópico:** `futbol.partidos.sensores_fatiga.v1`
* **Justificación:** Se ha seguido el patrón de convención de nombres jerárquico estándar `dominio.subdominio.tipo.version` para garantizar la organización, escalabilidad y mantenibilidad del canal de mensajes. La elección se basa en:
  * **Dominio (`futbol`):** Define el área de negocio o macro-categoría principal (preparando el clúster por si en el futuro se integran datos de otro deporte).
  * **Subdominio (`partidos`):** Establece el contexto de recolección de los datos, separándolos claramente de otras sesiones como `entrenamientos` o `pruebas_medicas`.
  * **Tipo (`sensores_fatiga`):** Identifica el evento específico y la naturaleza de las mediciones (coordenadas, velocidad, aceleración y ritmo cardíaco).
  * **Versión (`v1`):** Es una buena práctica fundamental que permite la evolución del esquema en el futuro (por ejemplo, si se añade un sensor de temperatura corporal en la `v2`) sin romper los consumidores que dependen del formato actual.

### 2.2. Esquema de los Mensajes
Los datos se transmiten utilizando una estructura JSON, garantizando el orden, la trazabilidad de cada evento y la portabilidad de los datos a lo largo de todo el pipeline.

* **La Clave (Key):** Se ha utilizado el identificador del jugador (`player_id`). 
  * *Motivo:* Al asignar una clave específica, Kafka garantiza mediante su función de *hashing* que todos los mensajes con el mismo `player_id` se enruten siempre a la misma partición dentro del tópico. Esto es crítico en arquitecturas de streaming, ya que asegura que los eventos de un mismo jugador se procesen en orden estrictamente secuencial (FIFO). Si la clave fuera nula, los mensajes se distribuirían en *Round-Robin* por todas las particiones, perdiendo la garantía de orden y arruinando los cálculos temporales posteriores.
* **El Timestamp:** Se ha configurado para extraerse directamente de la columna temporal del dataset original (Event Time) convertido a milisegundos, en lugar de usar el tiempo en el que Kafka recibe el mensaje (Processing Time). Esto asegura la precisión temporal del simulador, incluso frente a posibles retrasos en la red.
* **El Valor (Value):** Estructura en formato JSON. Como buena práctica de arquitectura de datos (Self-contained payload), se ha inyectado explícitamente el `timestamp` dentro del cuerpo del mensaje. De esta forma, el dato mantiene su integridad temporal incluso si posteriormente es exportado fuera del ecosistema de Kafka (por ejemplo, a un Data Lake). Adicionalmente, se ha incluido la versión del esquema y un identificador único y universal para cada evento (`event_id`) generado mediante la librería `uuid`.

**Ejemplo del Payload:**
```json
{
  "schema_version": "1.0",
  "event_id": "c1b52a36-3b49-410a-b31f-0e24106512eb",
  "match_id": 1,
  "session_id": "match_1",
  "timestamp": 1711209600000,
  "bpm": 145,
  "pos_x": 45.2,
  "pos_y": 34.1,
  "speed_kmh": 21.5,
  "acceleration_ms2": 1.2
}
```



## 3. Guía de Despliegue y Ejecución

### 3.1. Requisitos del Entorno
Para ejecutar este proyecto, es necesario contar con el siguiente entorno:
* Contenedor Docker configurado (ej. `jupyter/pyspark-notebook`).
* Python 3.x.
* Apache Kafka y Zookeeper corriendo en `localhost:9092`.

### 3.2. Instalación de Dependencias
Dado que los contenedores son efímeros, antes de lanzar los scripts es obligatorio instalar la librería cliente de Kafka. Abre una terminal en el entorno y ejecuta:

```bash
pip install kafka-python pandas
```

### 3.3. Ejecución del Sistema
Para simular el partido en tiempo real, se requiere la ejecución concurrente de los siguientes scripts en terminales independientes:

1. **Lanzar el Producer:**
Abre una terminal y ejecuta el simulador. Este script leerá el archivo CSV y comenzará a enviar ráfagas de datos a Kafka.
```bash
python producer.py
```

2. **Lanzar el Consumidor de Monitorización:**
En una segunda terminal, lanza el consumidor estándar para visualizar el flujo de datos en crudo.
```bash
python consumer_print.py
```

3. **Lanzar el Consumidor de Alertas:**
En una tercera terminal, ejecuta el sistema de alertas. Este script filtrará en tiempo real [RELLENAR: Tu novia debe poner aquí una frase explicando brevemente qué hace su consumidor, por ejemplo: "las pulsaciones mayores a 180"].
```bash
python consumer_alert.py
```

*(Nota: Para detener cualquier proceso de forma segura y cerrar las conexiones, pulsa `Ctrl + C` en su respectiva terminal).*

---

## 4. Demostración del Sistema (Vídeo)
A continuación, se adjunta un vídeo demostrativo donde se puede observar la arquitectura funcionando en tiempo real de forma paralela:

{{< video [URL_DEL_VIDEO_AQUÍ] >}}