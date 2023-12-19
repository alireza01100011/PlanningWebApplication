from pickle import loads, dumps

class _Task:
    __slots__ = ["id", "name", "time_start", "time_end", "done"]
    def __init__(self, id:int,
                 name:str , time_start:int, time_end:int, done:bool=False)-> None:
        self.id = id
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        self.done = done


class Tasks:
    def __init__(self):
        self.tasks:dict[int, _Task] = dict()
    #  End Function
    
    @property
    def list_tasks(self)-> list[_Task]:
        return [
            task for task in self.tasks.values()]

    @property
    def return_tasks_in_pickle(self)-> str:
        return dumps(self.list_tasks)
    #  End Function

    def set_tasks(self, tasks:list[_Task] )-> None:
        for task in tasks: self.tasks[task.id] = task
    #  End Function
        
    def action_add_task(self, name:str, time_start:int, time_end:int)-> None:
        _id = len(self.tasks) + 1
        self.tasks[_id] = _Task(_id ,name, time_start, time_end)
    #  End Function
        
    def action_done(self, id:int):
        self.tasks[id].done = not self.tasks[id].done
    #  End Function
        
    def action_update(self, id:int, name:str, time_start:int, time_end:int):
        _task = self.tasks.get(id)
        _task.name = name 
        _task.time_start, _task.time_end = time_start, time_end 
        self.tasks[id] =  _task; del _task
    #  End Function 
        
    def action_delete(self, id:int)-> None:
        del self.tasks[id]
    #  End Function
        
if __name__ == '__main__':
    t = Tasks()
    t.action_add_task('a', 545,545)
    print(t.tasks[1].done)
    t.action_done(1)
    print(t.tasks[1].done)
    t.action_done(1)
    print(t.tasks[1].done)