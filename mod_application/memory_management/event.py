"""
Events manager

- Add Event
- Update Event
- Remove Event
- Making a pickle to store in the database

"""

from pickle import loads, dumps

from group import _Group
class _Event():
    __slots__ = ['id', 'title', 'description', 'start_time',
                 'end_time', 'color', 'group_id', 'reminders']
    
    def __init__(self, id:int, title:str, description:str,
                 start_time:int, end_time:int, group:None|_Group,
                 reminders:list[int], color:str):
        self.id = id
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.reminders = reminders
        self.color = color

        if group : self.group_id = group.id
        else : self.group_id = 0


class EventManager():
    def __init__(self):
        self.events:dict[int, _Event] = dict()
        self.last_id = 0
    #  End Function
        
    @property
    def list_events(self):
        return [event 
                for event in self.events.values()]
    #  End Function

    @property
    def return_events_in_pickle(self):
        return dumps(self.list_events)
    #  End Function

    def set_events(self, events:list[_Event]):
        for event in events : self.events[event.id] = event
        self.last_id = len(self.events)
    #  End Function

    def add_event(self, title:str, description:str,
                 start_time:int, end_time:int, group:None,
                 reminders:list[int], color:str):
        
        while True:
            self.last_id += 1
            if not self.events.get(self.last_id):
                break
        
        self.events[self.last_id] = \
            _Event(
                id=self.last_id, title=title, group=group,
                description=description, end_time=end_time,
                start_time=start_time, reminders=reminders,
                color=color)
    #  End Function

    def delete_event(self, id:int):
        if self.events.get(id):
            del self.events[id]
    #  End Function

    def update_event(self, id:int,
                     title:str=None, reminders:list[int]=None,
                     description:str=None, start_time:int=None,
                     end_time:int=None, group_id:None=0,
                     color:str=None)-> None | KeyError:
        
        if not self.events.get(id):
            raise KeyError
        
        _event = self.events[id]
        _event.title = title or _event.title
        _event.description = description or _event.description
        _event.color = color or _event.color
        _event.start_time = start_time or _event.start_time
        _event.end_time = end_time or _event.end_time
        _event.group_id = group_id or _event.group_id
        _event.reminders = reminders or _event.reminders

        # Save
        self.events[id] = _event ; del _event
    #  End Function

if __name__ == '__main__':
    event_manager = EventManager()