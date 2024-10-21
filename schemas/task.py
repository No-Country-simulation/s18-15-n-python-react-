def taskDescription(item)-> dict:
    return {
            "id": str(item["_id"]),
            "name": item["name"],
            "descripcion": item["description"],
            "date_limit": item["date_limit"],
            "date_finish": item["date_finish"],
            "priority": item["priority"],
            "urgency": item["urgency"],
            "category": item["category"],
            "remindir": item["remindir"],
            
        }

def taskEntetity(entity) -> list:
    return [taskDescription(item) for item in entity]