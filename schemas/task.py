def taskDescription(item)-> dict:
    return {
            "id": str(item["_id"]),
            "title": item["title"],
            "description": item["description"],
            "fecha_termino": item["fecha_termino"],
            "fecha_finalizado": item["fecha_finalizado"],
            "carpeta": item["carpeta"],
            "prioridad": item["prioridad"],
            "terminado": item["terminado"],

            
        }

def taskEntetity(entity) -> list:
    return [taskDescription(item) for item in entity]