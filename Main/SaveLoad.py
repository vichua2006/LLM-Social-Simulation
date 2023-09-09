from typing import Tuple
import json
from Main.Individual import Individual, SeralizeQueue
from Main.System import System
from GUI.CustomConsoleLog import CustomConsoleLog

import jsonpickle
import jsonpickle.handlers
import datetime
import csv


# Serialize System object and console log to JSON
def save(system: System, console_log: str, filename: str):
    serialized_system = jsonpickle.encode(system)
    save_dict = {
        "system": serialized_system,
        "console_log": console_log
    }
    with open(filename, 'w') as f:
        json.dump(save_dict, f)
     
     

# def flatten_json_key(y): 
#     out = []
#     def flatten(x, name='', this_name=''): 
#         if type(x) is dict: 
#             for a in x: 
#                 flatten(x[a], name + a + '_', a) 
#         else: 
#             out.append(this_name)
#         flatten(y)
#     return out

# def flatten_json_value(y): 
#     out = []
#     def flatten(x, name=''): 
#         if type(x) is dict: 
#             for a in x: 
#                 flatten(x[a], name + a + '_') 
#         else: 
#             out.append(x)
#         flatten(y)
#     return out


file_name='Log/'+datetime.datetime.now().strftime("%B %d, %I %M%p , %Y")+'Experimentlog.csv'

def init_save(system: System):
    # serialized_system = jsonpickle.encode(system)
    # json_iteratable = json.loads(serialized_system)
    save_dict_day = []
    
    
    # TODO: most current
    # def custom_dict_repr_key(obj, key=''):
    #     if isinstance(obj, (int, float, str, bytes, bool, type(None))):
    #         if not isinstance(obj, (type(None))):
    #             save_dict_day.append(key)
    #     elif isinstance(obj, (list, tuple)):
    #         save_dict_day.append(key)
    #     elif isinstance(obj, SeralizeQueue):
    #         return None
    #     elif isinstance(obj, CustomConsoleLog):
    #         return None
    #     elif isinstance(obj, dict):
    #         for k, v in obj.items():
    #             custom_dict_repr_key(v, k)
    #     else:
    #         variables = vars(obj)
    #         for k, v in variables.items():
    #             custom_dict_repr_key(v, k)
    
    
    # for person in system.individuals:
    #     for key, item in person.__dict__.items():
    #         if isinstance(item, dict):
    #             for key_, item_ in item:
    #                 save_dict_day.append(key_)
    #         save_dict_day.append(key)

    # with open(temp_json_file_name, 'w+') as temp:
    #     json_file = json.dump(serialized_system, temp)
    # with open(temp_json_file_name, 'r+') as temp:
    
    # item_lists= flatten_json_key(json_iteratable)
    
    custom_dict_repr_key(system, 'system')
    with open(file_name, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(save_dict_day)

def save_logframes(system: System):
    # serialized_system = jsonpickle.encode(system)
    # json_iteratable = json.loads(serialized_system)
    # item_lists = flatten_json_value(json_iteratable)
    # if len(system.individuals)==0:
    #     return ''
    
    save_dict_day = []
    # save_dict_day.append()
    
    # DOTO: most current
    # # for person in system.individuals:
    # #     for key, item in person.__dict__.items():
    # #         save_dict_day.append(item)
    # def custom_dict_repr_val(obj, key=''):
    #     if isinstance(obj, (int, float, str, bytes, bool, type(None))):
    #         if not isinstance(obj, (type(None))):
    #             save_dict_day.append(obj)
    #     elif isinstance(obj, (list, tuple)):
    #         save_dict_day.append(obj)
    #     elif isinstance(obj, SeralizeQueue):
    #         return None
    #     elif isinstance(obj, CustomConsoleLog):
    #         return None
    #         # return [custom_dict_repr(e) for e in obj.queue]
    #     elif isinstance(obj, dict):
    #         for k, v in obj.items():
    #             custom_dict_repr_val(v, k)
    #     else:
    #         variables = vars(obj)
    #         for k, v in variables.items():
    #             custom_dict_repr_val(v, k)


    # custom_dict_repr_val(system, 'system')

    with open(file_name, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(save_dict_day)

# def init_save(system: System):
#     save_dict_day = []
#     for person in system.individuals:
#         for key, item in person.__dict__.items():
#             save_dict_day.append(key)
#     with open(file_name, 'a', newline='') as f:
#         csv_writer = csv.writer(f)
#         csv_writer.writerow(save_dict_day)

# #TODO: these things...
# def save_logframes(system: System):
#     serialized_system = jsonpickle.encode(system)
#     if len(system.individuals)==0:
#         return ''
    
#     save_dict_day = []
#     for person in system.individuals:
#         for key, item in person.__dict__.items():
#             save_dict_day.append(item)

#     with open(file_name, 'a', newline='') as f:
#         csv_writer = csv.writer(f)
#         csv_writer.writerow(save_dict_day)

# Deserialize System object and console log from JSON
def load(filename: str) -> Tuple[System, str]:
    with open(filename, 'r') as f:
        load_dict = json.load(f)
    
    loaded_system:System = jsonpickle.decode(load_dict["system"])
    loaded_console_log:str = load_dict["console_log"]
    return loaded_system, loaded_console_log

