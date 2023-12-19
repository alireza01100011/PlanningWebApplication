import unittest
import pickle

import todo_class

class TestTasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tasks = todo_class.Tasks()
        cls.add_n = 5
        for _i in range(1, cls.add_n):
            name, t_s, t_e = f'task_{_i}', 1702999710, 1702000000
            cls.tasks.action_add_task(name, t_s, t_e)

    def test_list_tasks(self):
        self.assertEqual(
            type(self.tasks.list_tasks), list)
        

    def test_action_delete(self):
        id = 2
        self.tasks.action_delete(id)
        
        self.assertEqual(
            self.tasks.tasks.get(id), None)
        
    def test_action_done(self):
        id = 1
        done = self.tasks.tasks[id].done
        self.tasks.action_done(id)

        self.assertNotEqual(done,
                            self.tasks.tasks[id].done)

    def test_action_update(self):
        id = 1
        name, t_s, t_e = 'update', 1,2
        self.tasks.action_update(id, name, t_s, t_e)
        task = self.tasks.tasks[id]
        self.assertEqual(task.id, id)
        self.assertEqual(task.name, name)
        self.assertEqual(task.time_start, t_s)
        self.assertEqual(task.time_end, t_e)
    
    def test_return_tasks_in_pickle(self):
        list_data = self.tasks.list_tasks
        _temp_p = self.tasks.return_tasks_in_pickle
        list_pikle = pickle.loads(_temp_p)
        self.assertEqual(len(list_data), len(list_pikle))

        
if __name__ == '__main__':
    unittest.main()
    