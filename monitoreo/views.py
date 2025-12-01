from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Dato

@csrf_exempt
def recibir_dato(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"})

    try:
        # Leer JSON enviado por mqtt_bridge.py
        data = json.loads(request.body.decode("utf-8"))

        municipio = data.get("ciudad")
        tipo = data.get("tipo")
        valor = data.get("valor")

        if not municipio or not tipo or valor is None:
            return JsonResponse({"error": "Faltan datos"})

        # Convertir valor a número si se puede
        try:
            valor = float(valor)
        except:
            pass  # Si no es número, lo dejamos como texto

        Dato.objects.create(
            municipio=municipio,
            tipo=tipo,
            valor=valor
        )

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"error": str(e)})


def api_data(request):
    data = {
        "temperatura": None,
        "humedad": None,
        "calidad": None,
    }

    ultimo_temp = Dato.objects.filter(tipo="temperatura").order_by("-timestamp").first()
    ultimo_hum = Dato.objects.filter(tipo="humedad").order_by("-timestamp").first()
    ultimo_cal = Dato.objects.filter(tipo="calidad").order_by("-timestamp").first()

    if ultimo_temp:
        data["temperatura"] = ultimo_temp.valor

    if ultimo_hum:
        data["humedad"] = ultimo_hum.valor

    if ultimo_cal:
        data["calidad"] = ultimo_cal.valor

    return JsonResponse(data)
