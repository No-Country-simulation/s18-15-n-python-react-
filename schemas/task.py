def taskDescription(item)-> dict:
    return {
            "name": item["name"],
            "descripcion": item["description"]
            
        }

def taskEntetity(entity)->list:
    [taskDescription(item) for item in entity]