import threading
import PySimpleGUI as sg
from typing import List, Tuple
import jsonpickle
from GUI.CustomConsoleLog import CustomConsoleLog
from GUI.ConsoleLog import ConsoleLog
from Main.Individual import Individual
from Main.SaveLoad import load, save
from Main.System import System
from Main.Simulation import initialize, simulate
from datetime import datetime
import sys

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'


def collapse(layout, key):
    return sg.pin(sg.Column(layout, key=key))
    
def create_individual_layout(individual: List[Individual]) -> sg.TabGroup:
    person_layout = []
    for i, person in enumerate(individual):
        section_key = f'-SECTION{i}-'
        pending_action_layout = [[sg.Listbox(values=person.get_pending_action_as_list(), size=(30, 5),  horizontal_scroll= True, key=f'-PENDINGACTION{i}-')]]
        obey_subject_layout = [[sg.Listbox(values = person.obey_stats.subject, size=(30, 5),  horizontal_scroll= True, key=f'-OBEYSUBJECT{i}-')]]
        memory_layout = [[sg.Listbox(values = person.memory, size=(30, 5),  horizontal_scroll= True, key=f'-MEMORY{i}-')]]
        rob_stat_layout = [[sg.Listbox(values = person.robbing_stats.get_rob_times_list(), size=(30, 5),  horizontal_scroll= True, key=f'-ROBTIMESLIST{i}-')]]
        left_section = [[sg.Text('Aggressiveness:'), sg.Input(person.attributes["aggressiveness"], size = (15, None), key=f'-AGGRESSIVENESS{i}-')],
                   [sg.Text('Covetousness:'), sg.Input(person.attributes["covetousness"], size = (15, None), key=f'-COVETOUSNESS{i}-')],
                   [sg.Text('Intelligence:'), sg.Input(person.attributes["intelligence"], size = (15, None), key=f'-INTELLIGENCE{i}-')],
                   [sg.Text('Strength:'), sg.Input(person.attributes["strength"], size = (15, None), key=f'-STRENGTH{i}-')],
                   [sg.Text('SocialPosition:'), sg.Input(person.attributes["social_position"], size = (10, None), key=f'-SOCIALPOSITION{i}-')],
                   [sg.Text('Food:'), sg.Input(person.attributes["food"], size = (10, None), key=f'-FOOD{i}-')],
                   [sg.Text('Land:'), sg.Input(person.attributes["land"], size = (10, None), key=f'-LAND{i}-')],
                   [sg.Text('Action:'), sg.Input(person.attributes["action"], size = (10, None), key=f'-Action{i}-')],
                   [sg.Text('CurrentActionType:'), sg.Input(person.current_action_type, size = (10, None), key=f'-CURRENTACTIONTYPE{i}-')],
                   [sg.Text('ObeyTo:'), sg.Input(person.obey_stats.obey_personId, size = (10, None), key=f'-OBEYPERSONID{i}-')],
                   [sg.Text('TotalRobTimes:'), sg.Input(person.robbing_stats.total_rob_times, size = (10, None), key=f'-TOTALROBTIMES{i}-')],
                   ]
        right_section = [[sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN PENDINGACTION-', text_color='white'), sg.T('Pending Action', enable_events=True, text_color='white', k='-OPEN PENDINGACTION-TEXT')],
                         [collapse(pending_action_layout, '-PENDINGACTION-')],
                         [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN OBEYSUBJECT-', text_color='white'), sg.T('Obey Subject', enable_events=True, text_color='white', k='-OPEN OBEYSUBJECT-TEXT')],
                         [collapse(obey_subject_layout, '-OBEYSUBJECT-')],
                         [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN MEMORY-', text_color='white'), sg.T('Memory', enable_events=True, text_color='white', k='-OPEN MEMORY-TEXT')],
                         [collapse(memory_layout, '-MEMORY-')],
                         ]
        new_left_section = [[sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN LEFTSEC-', text_color='white'), sg.T('Attibute', enable_events=True, text_color='white', k='-OPEN LEFTSEC-TEXT')],
                            [collapse(left_section, '-LEFTSEC-')],
                            [sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN ROBTXT-', text_color='white'), sg.T('RobTimes', enable_events=True, text_color='white', k='-OPEN ROBTXT-TEXT')],
                            [collapse(rob_stat_layout, '-ROBTXT-')]
                            ]

        left = sg.Column(new_left_section, size=(None, None))
        print(left.Size)
        section = [[left, sg.Column(right_section)]]
        person_layout.append(sg.Tab(f'Person {i}', section, key=section_key))
    return sg.TabGroup([person_layout])


def start_simulate(system:System):
    for i in range(25):
        print(f"DAY {system.time+1} HAS STARTED.")
        simulate(system.individuals, system)
def main():
    
    system=initialize()
    individuals = system.individuals
    
    person_layout = [[create_individual_layout(individuals)]]
    special_log_layout = [[sg.Multiline(size=(80,10), key='-SPECIAL OUTPUT-', autoscroll=False)]]
    layout_left = person_layout + special_log_layout
    console_log_layout = [[sg.Multiline(size=(80,30), key='-OUTPUT-', autoscroll=False)]]
    button_layout = [[sg.Button('Start', key= '-START-'), sg.Button('Stop', key= '-STOP-'), sg.Button('Clear', key= '-Clear-'), sg.Button('Exit', key= '-Exit-') ,sg.Button('Export', key= '-Export-'), sg.Button('Save', key= '-Save-') ,sg.Button('Load', key= '-Load-'), sg.Button('DEBUG', key= '-DEBUG-')]]
    layout_right = console_log_layout+ button_layout
    #column layout of person_layout and console_log_layout
    layout = [[sg.Column(layout_left), sg.Column(layout_right)]]
    window = sg.Window('LLM Social Simulation', layout)
    #redirect stdout to the sg.Output element
    sys.stdout = ConsoleLog(window, '-OUTPUT-', '-OUTPUT THREAD-')
    
    thread: threading.Thread
    system.set_console_log(CustomConsoleLog(window, '-SPECIAL OUTPUT-'))
    isappStarted = False
    opened = [True for i in range(10)]
        # Redirect stdout to the sg.Output element
    while True:             # Event Loop
        event, values = window.read(timeout=100) #update every 100ms
        if event == sg.WIN_CLOSED:
            break
        elif event == '-OUTPUT THREAD-':
            window['-OUTPUT-'].update(values['-OUTPUT THREAD-'], append = True)
        elif event == '-Clear-':
            window['-OUTPUT-'].update('')
        elif event == '-Exit-':
            system.is_stop = False
            isappStarted = False
            break
        elif event == '-START-':
            print("Start")
            system.is_stop=False
            if(isappStarted):
                continue
            thread = window.start_thread(lambda: start_simulate(system), ('-MAIN THREAD-', '-MAIN THREAD ENDED-'))
            isappStarted = True
        elif event == '-STOP-':
            system.is_stop=True
            print("Stop")
            isappStarted = False
        elif event == '-Export-':
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            folderPath = "Log"
            filename = f"{folderPath}/{current_time}.txt"
            with open(filename, 'w') as f:
                f.write(window['-OUTPUT-'].get())
            print(f"Log successfully export to {filename}")
        elif event == '-Save-':
            filepath = sg.popup_get_file('Save File', save_as=True, no_window=True, file_types=(("Simulation Save", "*.txt"),))
            if filepath:
                console_log = window['-OUTPUT-'].get()
                save(system, console_log, filepath)
                # Save the console log
                print(f"Log successfully saved to {filepath}")
        if event.startswith('-OPEN LEFTSEC-'):
            opened[0] = not opened[0]
            window['-OPEN LEFTSEC-'].update(SYMBOL_DOWN if opened[0] else SYMBOL_UP)
            window['-LEFTSEC-'].update(visible=opened[0])
            # if(not opened1):
            #     window['-LEFTSEC-'].Widget
        if event.startswith('-OPEN RIGHTSEC-'):
            opened[1] = not opened[1]
            window['-OPEN RIGHTSEC-'].update(SYMBOL_DOWN if opened[1] else SYMBOL_UP)
            window['-RIGHTSEC-'].update(visible=opened[1])
        if event.startswith('-OPEN ROBTXT-'):
            opened[2] = not opened[2]
            window['-OPEN ROBTXT-'].update(SYMBOL_DOWN if opened[2] else SYMBOL_UP)
            window['-ROBTXT-'].update(visible=opened[2])
        if event.startswith('-OPEN PENDINGACTION-'):
            opened[3] = not opened[3]
            window['-OPEN PENDINGACTION-'].update(SYMBOL_DOWN if opened[3] else SYMBOL_UP)
            window['-PENDINGACTION-'].update(visible=opened[3])
        if event.startswith('-OPEN OBEYSUBJECT-'):
            opened[4] = not opened[4]
            window['-OPEN OBEYSUBJECT-'].update(SYMBOL_DOWN if opened[4] else SYMBOL_UP)
            window['-OBEYSUBJECT-'].update(visible=opened[4])
        if event.startswith('-OPEN MEMORY-'):
            opened[5] = not opened[5]
            window['-OPEN MEMORY-'].update(SYMBOL_DOWN if opened[5] else SYMBOL_UP)
            window['-MEMORY-'].update(visible=opened[5])
        
        elif event == '-Load-':
            system.is_stop=True
            print("Stop")
            isappStarted = False
            
            filepath = sg.popup_get_file('Load File', save_as=False, no_window=True, file_types=(("Simulation Save", "*.txt"),))
            if filepath:
                system, console_log = load(filepath)
                individuals = system.individuals
                window['-OUTPUT-'].update(console_log)
                print(f"{filepath} successfully loaded")
        elif event == '-DEBUG-':
            print("DEBUG")

        
        
        
        #update 
        #update console log
        window[f'-OUTPUT-'].update()
        
        for i, person in enumerate(individuals):
            #Update person attributes
            window[f'-AGGRESSIVENESS{i}-'].update(person.attributes["aggressiveness"])
            window[f'-COVETOUSNESS{i}-'].update(person.attributes["covetousness"])
            window[f'-INTELLIGENCE{i}-'].update(person.attributes["intelligence"])
            window[f'-STRENGTH{i}-'].update(person.attributes["strength"])
            window[f'-SOCIALPOSITION{i}-'].update(person.attributes["social_position"])
            window[f'-FOOD{i}-'].update(person.attributes["food"])
            window[f'-LAND{i}-'].update(person.attributes["land"])
            window[f'-Action{i}-'].update(person.attributes['action'])
            window[f'-CURRENTACTIONTYPE{i}-'].update(person.current_action_type)
            window[f'-OBEYPERSONID{i}-'].update(person.obey_stats.obey_personId)
            window[f'-SPECIAL OUTPUT-'].update(system.console_log.content)
            window[f'-ROBTIMESLIST{i}-'].update(person.robbing_stats.get_rob_times_list())

            # Update Listbox, Remain the listbox scroll position
            for key in [f'-PENDINGACTION{i}-', f'-OBEYSUBJECT{i}-', f'-MEMORY{i}-']:
                # Access the tkinter Listbox widget
                lb_widget = window[key].Widget

                # Get current scroll position
                scroll_position = lb_widget.yview()
                match key:
                    case _ if (_ := f'-PENDINGACTION{i}-') == key:
                        new_values = person.get_pending_action_as_list()
                    case _ if (_ := f'-OBEYSUBJECT{i}-') == key:
                        new_values = person.obey_stats.subject
                    case _ if (_ := f'-MEMORY{i}-') == key:
                        new_values = person.memory
                
                
                window[key].update(new_values)
            
                # Set the scroll position to the previous position
                lb_widget.yview_moveto(scroll_position[0])
            
        window.refresh()
            

    window.close()

if __name__ == "__main__":
    main()
