import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime, timedelta, timezone
from db import user_collection, task_collection
from bson import ObjectId
from pytz import timezone as pytz_timezone

# Cargar variables de entorno
load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Usamos SMTP_SSL con el puerto 465

# Función para enviar el correo
async def enviar_correo_notificacion(to_email: str, tarea):
    task_title = tarea["title"]
    
    # Obtener la zona horaria del usuario
    user = await user_collection.find_one({"_id": ObjectId(tarea["user_id"])})
    user_tz = pytz_timezone(user['timezone'])  # Convertir la cadena de zona horaria a un objeto de zona horaria
    
    # Convertir la fecha de vencimiento a la zona horaria local del usuario
    due_date_utc = tarea["fecha_termino"]
    due_date_local = due_date_utc.astimezone(user_tz)
    
    # Formatear la fecha de vencimiento
    due_date = due_date_local.strftime("%Y-%m-%d %H:%M")  

    # Crear el mensaje de correo
    em = EmailMessage()
    em["From"] = f"Planifica+ <{EMAIL_USER}>"  # Personalizamos el remitente
    em["To"] = to_email
    em["Subject"] = f"Recordatorio: la tarea '{task_title}' vence pronto"
    
    # Cuerpo del correo
    body = f"¡Hola!\n\nLa tarea '{task_title}' tiene como fecha límite el {due_date}.\nNo olvides completarla."
    em.set_content(body)

    # Conectar al servidor SMTP y enviar el correo
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
            print("Iniciando conexión SMTP...")
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, to_email, em.as_string())
            print(f"Correo enviado a {to_email} para la tarea '{task_title}'")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
    return True


# Función para revisar las tareas que vencen y enviar notificaciones
async def revisar_tareas_vencimiento():
    now = datetime.now(timezone.utc)
    next_24_hours = now + timedelta(hours=24)

    print(f"Verificando tareas entre {now.isoformat()} y {next_24_hours.isoformat()}") 

    # Buscar tareas que venzan en las próximas 24 horas y que no hayan sido notificadas
    tareas_a_vencer = await task_collection.find({
        "fecha_termino": {"$lte": next_24_hours, "$gte": now},
        "notifiqued": False,
        "terminado": False
    }).to_list(length=None)

    print("Tareas encontradas para notificación:", tareas_a_vencer)

    if tareas_a_vencer:
        print(f"Se encontraron {len(tareas_a_vencer)} tareas que vencen pronto:")
        for tarea in tareas_a_vencer:
            print(f"- Título: {tarea['title']}, Fecha de vencimiento: {tarea['fecha_termino']}, ID de usuario: {tarea['user_id']}")
    else:
        print("No se encontraron tareas que vencen en las próximas 24 horas.")

    all_tasks = await task_collection.find({"terminado": False}).to_list(length=None)
    for tarea in all_tasks:
        fecha_termino = tarea.get("fecha_termino")
        if fecha_termino is not None:  # Verifica que fecha_termino no sea None
            # Asegúrate de que fecha_termino sea offset-aware
            if fecha_termino.tzinfo is None:
                fecha_termino = fecha_termino.replace(tzinfo=timezone.utc)
            print(f"Tarea: {tarea['title']}, Fecha de vencimiento: {fecha_termino}, Comparación: {now <= fecha_termino <= next_24_hours}")
        else:
            print(f"Tarea: {tarea['title']} tiene una fecha de vencimiento no definida.")

    for tarea in tareas_a_vencer:
        user = await user_collection.find_one({"_id": ObjectId(tarea["user_id"])})
        if user:
            # Enviar notificación de correo
            if await enviar_correo_notificacion(user["email"], tarea):
                # Actualizar la tarea para marcarla como notificada solo si el envío fue exitoso
                await task_collection.update_one(
                    {"_id": tarea["_id"]},
                    {"$set": {"notifiqued": True}}
                )
                print(f"Correo notificado para la tarea '{tarea['title']}' a {user['email']}.")
            else:
                print(f"No se pudo enviar el correo para la tarea '{tarea['title']}' a {user['email']}. No se actualizará el estado.")
