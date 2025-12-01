import paho.mqtt.client as mqtt
from monitoreo.models import Dato
from threading import Thread

CACHE = {}

BROKER = "broker.hivemq.com"
TOPIC = "sonora/#"


def on_connect(client, userdata, flags, rc):
    print("MQTT conectado. Código:", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print("MQTT recibido:", msg.topic, payload)

        # Tópico: sonora/<municipio>/<tipo>
        parts = msg.topic.split("/")
        municipio = parts[1]
        tipo = parts[2]  # temperatura | humedad | calidad
        valor = float(payload)

        # Guardar en caché (para mostrar en el dashboard)
        CACHE[tipo] = valor

        # Guardar en BD según el tipo
        if tipo == "temperatura":
            Dato.objects.create(municipio=municipio, tipo="temperatura", valor=valor)

        elif tipo == "humedad":
            Dato.objects.create(municipio=municipio, tipo="humedad", valor=valor)

        elif tipo == "calidad":
            Dato.objects.create(municipio=municipio, tipo="calidad", valor=valor)

        else:
            print("⚠ Tipo de sensor no reconocido:", tipo)

    except Exception as e:
        print("Error MQTT:", e)


def start():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_forever()


def run():
    t = Thread(target=start)
    t.daemon = True
    t.start()
