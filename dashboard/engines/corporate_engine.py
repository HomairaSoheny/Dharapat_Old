def getCIBCategory(cib):
    category_mapping = {
        "Type a": "Type a",
        "Type b": "Type b",
        "Type c": "Type c",
        "Type d": "Type d",
        "Type e": "Type e",
        "Type f": "Type f",
        "Type g": "Type g",
        "Type h": "Type h",
        "Type i": "Type i"
    }

    return category_mapping.get(cib.cib_category, None)