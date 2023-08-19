def capitalize(value: str):
    if len(value) > 1:
        return value[0].upper() + value[1:]
    elif value:
        return value.upper()
    else:
        return value
