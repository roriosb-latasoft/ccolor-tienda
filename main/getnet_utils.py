import requests
import hashlib
import base64
from datetime import datetime, timedelta
import pytz

def crear_sesion_pago(referencia, monto, return_url):
    # Configuración inicial
    GETNET_LOGIN = "7ffbb7bf1f7361b1200b2e8d74e1d76f"  # Reemplaza con tu login
    GETNET_SECRET_KEY = "SnZP3D63n3I9dH9O"  # Reemplaza con tu secretKey
    GETNET_URL_BASE = "https://checkout.test.getnet.cl"  # Ambiente de pruebas

    # Generar autenticación
    seed = datetime.now(pytz.UTC).isoformat()  # Fecha en formato ISO 8601
    nonce = base64.b64encode(hashlib.sha256(seed.encode()).digest()).decode()  # Valor aleatorio
    tranKey = base64.b64encode(hashlib.sha256(f"{nonce}{seed}{GETNET_SECRET_KEY}".encode()).digest()).decode()  # Llave transaccional

    auth = {
        "login": GETNET_LOGIN,
        "tranKey": tranKey,
        "nonce": nonce,
        "seed": seed,
    }

    # Datos de la solicitud
    data = {
        "auth": auth,
        "locale": "es_CL",  # Idioma y región (puedes cambiarlo según tus necesidades)
        "payment": {
            "reference": referencia,  # Referencia única
            "description": "Compra en mi tienda",  # Descripción del pago
            "amount": {
                "currency": "CLP",  # Moneda (cambia si es necesario)
                "total": float(monto),  # Total a pagar
            }
        },
        "expiration": (datetime.now() + timedelta(minutes=15)).isoformat(),  # Expiración de la sesión
        "returnUrl": return_url,  # URL de retorno tras el pago
        "ipAddress": "127.0.0.1",  # Dirección IP del cliente (puedes hacerlo dinámico si es necesario)
        "userAgent": "DjangoApp/1.0",  # Identificador del cliente
    }

    # Enviar solicitud a la API de Getnet
    try:
        url = f"{GETNET_URL_BASE}/api/session/"
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            return response.json()  # Devuelve la respuesta en formato JSON (contiene processUrl y requestId)
        else:
            return {"error": response.text}  # Devuelve el error si ocurre algo
    except Exception as e:
        return {"error": str(e)}  # Manejo de errores genéricos