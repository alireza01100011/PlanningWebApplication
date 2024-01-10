from pickle import dumps, loads

class _Group(object):
    __slots__ = ['id', 'title', 'description', 'color']

    def __init__(self, id:int, title:str,
                 description:str, color:str):
        self.id = id
        self.title = title
        self.description = description
        self.color = color


class GroupManager():
    def __init__(self, pickle_data:bytes=None):
        self.groups:dict[int, _Group] = dict()
        self.last_id = 1
        
        # Default
        self.groups[0] = _Group(
                id=0,
                title='defualt',
                description='default',
                color='#ffff')
        
        if pickle_data:    
            self.set_groups(loads(pickle_data))


    #  End Function
        
    @property
    def list_groups(self):
        return [group 
                for group in self.groups.values()]
    #  End Function

    @property
    def return_group_in_pickle(self):
        return dumps(self.list_groups)
    #  End Function
        
    def set_groups(self, groups:list[_Group]):
        self.groups = dict()
        for _g in groups : self.groups[_g.id] = _g
        self.last_id = len(groups)
    #  End Function
        
    def add_group(self, title:str, color:str,
                 description:str)-> int :
       while True:
           self.last_id += 1
           if not self.groups.get(self.last_id):
               break
        
       self.groups[self.last_id] = \
            _Group(
                id=self.last_id, title=title,
                description=description, color=color)
       
       return self.last_id
    #  End Function

    def update_group(self, id:int, 
                     title:str=None, description:str=None,
                     color:str=None)-> None | KeyError:
        
        if not self.groups.get(id):
            raise KeyError

        _group = self.groups[id]
        _group.title = title or _group.title
        _group.description = description or _group.description
        _group.color = color or _group.color

        self.groups[id] = _group; del _group
    #  End Function
        
    def delete_group(self, id:int)-> KeyError | None:
        if not self.groups.get(id):
            raise KeyError
        del self.groups[id]
    #  End Function

