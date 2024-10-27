import httpx

async def get_timezone(ip: str) -> str:
    """Obtiene la zona horaria basada en la dirección IP de manera asíncrona."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{ip}")
            data = response.json()

        if response.status_code == 200 and data['status'] == 'success':
            return data.get('timezone')  # Devolver la zona horaria
        else:
            print("Error al obtener la información:", data.get('message', ''))
            return None
    except Exception as e:
        print("Excepción al obtener la zona horaria:", str(e))
        return None
