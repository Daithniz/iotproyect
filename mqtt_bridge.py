import json
import requests
import paho.mqtt.client as mqtt

API_URL = "http://127.0.0.1:8000/monitoreo/recibir/"

def on_message(client, userdata, msg):
    try:
        raw = msg.payload.decode()

        # Espera formato: ciudad | tipo | valor
        partes = [p.strip() for p in raw.split("|")]

        if len(partes) != 3:
            print("Formato inválido:", raw)
            return

        municipio, tipo, valor = partes

        print(f"Recibido MQTT → {municipio} | {tipo} | {valor}")

        # Construir JSON correcto
        payload = {
            "ciudad": municipio,
            "tipo": tipo,
            "valor": valor
        }

        r = requests.post(API_URL, json=payload)

        print("Respuesta Django:", r.text)

    except Exception as e:
        print("Error procesando mensaje:", e)


client = mqtt.Client()
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

# Suscripción al topic correcto
client.subscribe("sonora/sensores")

print("Escuchando MQTT...")
client.loop_forever()
