from datetime import datetime
import pytz

def convert_to_utc(local_dt: datetime, timezone_str: str) -> datetime:
    """Convierte un datetime local a UTC usando la zona horaria especificada."""
    local_tz = pytz.timezone(timezone_str)
    local_dt = local_tz.localize(local_dt)  # Localizar el datetime local
    return local_dt.astimezone(pytz.utc)  # Convertir a UTC

def convert_to_local(utc_dt: datetime, timezone_str: str) -> datetime:
    """Convierte un datetime en UTC a la zona horaria local especificada."""
    utc_dt = pytz.utc.localize(utc_dt)  # Localizar el datetime UTC
    local_tz = pytz.timezone(timezone_str)
    return utc_dt.astimezone(local_tz)  # Convertir a la zona horaria local
