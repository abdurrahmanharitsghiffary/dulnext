def get_nested(d, keys):
    for key in keys:
        d = d.get(key)
        if d is None:
            return None
    return d
