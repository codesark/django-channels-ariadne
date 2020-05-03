
def map_attrs_to_dict(obj, attrs=[]):
    return {attr: getattr(obj, attr) for attr in attrs}
