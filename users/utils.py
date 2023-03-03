def nested_dict_values(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from nested_dict_values(v)
        else:
            yield v
