from datetime import datetime

def string_to_int(_time:str, fromat:str='%Y-%m-%d %H:%M')->str :
    res = datetime.strptime(_time, "%Y-%m-%d %H:%M").timestamp()
    return f'{int(res)}000'