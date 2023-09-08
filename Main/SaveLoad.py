from typing import Tuple
import json
from Main.Individual import Individual
from Main.System import System
import jsonpickle
import jsonpickle.handlers

# Serialize System object and console log to JSON
def save(system: System, console_log: str, filename: str):
    serialized_system = jsonpickle.encode(system)
    save_dict = {
        "system": serialized_system,
        "console_log": console_log
    }
    with open(filename, 'w') as f:
        json.dump(save_dict, f)
     
file_name='Log/'+datetime.datetime.now().strftime("%B %d, %I %M%p , %Y")+'Experimentlog.csv'
def init_save(system: System):
    save_dict_day = []
    for person in system.individuals:
        for key, item in person.__dict__.items():
            save_dict_day.append(key)
    with open(file_name, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(save_dict_day)

#TODO: these things...
def save_logframes(system: System):
    serialized_system = jsonpickle.encode(system)
    if len(system.individuals)==0:
        return ''
    
    save_dict_day = []
    for person in system.individuals:
        for key, item in person.__dict__.items():
            save_dict_day.append(item)

    with open(file_name, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(save_dict_day)

# Deserialize System object and console log from JSON
def load(filename: str) -> Tuple[System, str]:
    with open(filename, 'r') as f:
        load_dict = json.load(f)
    
    loaded_system:System = jsonpickle.decode(load_dict["system"])
    loaded_console_log:str = load_dict["console_log"]
    return loaded_system, loaded_console_log

