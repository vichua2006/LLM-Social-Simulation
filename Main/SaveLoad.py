import json
import queue
from Main.Individual import Individual
from Main.System import System
import jsonpickle
import jsonpickle.handlers

class QueueHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        data['items'] = list(obj.queue)
        return data

    def restore(self, obj):
        q = queue.Queue()
        for item in obj['items']:
            q.put(item)
        return q
# Register the custom handler for queue.Queue
jsonpickle.handlers.register(queue.Queue, QueueHandler)

# Serialize System object to JSON
def save_system(system: System, filename: str):
    serialized_system = jsonpickle.encode(system)
    with open(filename, 'w') as f:
        f.write(serialized_system)

# Deserialize System object from JSON
def load_system(filename: str) -> System:
    with open(filename, 'r') as f:
        loaded_serialized_system = f.read()
    loaded_system = jsonpickle.decode(loaded_serialized_system)
    return loaded_system

