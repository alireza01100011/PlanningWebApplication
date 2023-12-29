def _get_fields(obj):
    fields = [_ for _ in obj._fields]
    return [getattr(obj , _ ) for _ in fields]