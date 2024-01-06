""" 
Manages tasks (Todos)

- Add Task
- Update Task
- Remove
- Done Task
- Making a pickle to store in the database

"""
from pickle import loads, dumps

class _Task:
    __slots__ = ["id", "name", "time_start", "done"]
    def __init__(self, id:int,
                 name:str , time_start:int, done:bool=False)-> None:
        self.id = id
        self.name = name
        self.time_start = time_start
        self.done = done


class TasksManager:
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
        
    def add_task(self, name:str, time_start:int)-> None:
        _id = len(self.tasks) + 1
        self.tasks[_id] = _Task(_id ,name, time_start)
    #  End Function
        
    def done_task(self, id:int):
        self.tasks[id].done = not self.tasks[id].done
    #  End Function
        
    def update_task(self,
                    id:int, name:str=None,
                    time_start:int=None):
        _task = self.tasks.get(id)
        _task.name = name or _task.name 
        _task.time_start = time_start or _task.time_start
        self.tasks[id] = _task; del _task
    #  End Function 
        
    def delete_task(self, id:int)-> None:
        del self.tasks[id]
    #  End Function
        
if __name__ == '__main__':
    t = TasksManager()
    t.add_task('a', 545)
    print(t.tasks[1].done)
    t.done_task(1)
    print(t.tasks[1].done)
    t.done_task(1)
    print(t.tasks[1].done)