from typing import Tuple
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

# Serialize System object and console log to JSON
def save(system: System, console_log: str, filename: str):
    serialized_system = jsonpickle.encode(system)
    save_dict = {
        "system": serialized_system,
        "console_log": console_log
    }
    with open(filename, 'w') as f:
        json.dump(save_dict, f)

# Deserialize System object and console log from JSON
def load(filename: str) -> Tuple[System, str]:
    with open(filename, 'r') as f:
        load_dict = json.load(f)
    
    loaded_system = jsonpickle.decode(load_dict["system"])
    loaded_console_log = load_dict["console_log"]
    return loaded_system, loaded_console_log

