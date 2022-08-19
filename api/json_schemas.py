create_receipt = {
    "type": "object",
    "properties": {
        "store":        {"type": "string"},
        "comment":      {"type": "string"},
        "timestamp":    {"type": "integer"},
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