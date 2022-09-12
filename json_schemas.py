create_receipt = {
    "type": "object",
    "properties": {
        "store":        {"type": "string"},
        "comment":      {"type": "string"},
        "timestamp":    {"type": "integer"},
        "category":     {"type": "string"},
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"},
                    "price": {"type": "number"},
                    "quantity": {"type": "number"}
                },
                "required": ["item", "price", "quantity"]
            }
        }
    },
    "required": ["products"]
}

register_user = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "fname":    {"type": "string"},
        "lname":    {"type": "string"},
        "logon_allowed": {"type": "boolean"}
    },
    "required": ["username", "password"]
}