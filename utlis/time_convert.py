from datetime import datetime

def string_to_int(_time:str, format:str='%Y-%m-%d %H:%M', _add:str='000')->str :
    res = datetime.strptime(_time, f'{format}').timestamp()
    return f'{int(res)}{_add}'