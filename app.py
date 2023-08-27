import sys
import threading
import PySimpleGUI as sg
from typing import List, Tuple
from GUI.CustomConsoleLog import CustomConsoleLog
from Main.Individual import Individual, System
from Main.Simulation import initialize, simulate
from datetime import datetime
import time
    
def create_individual_layout(individual: List[Individual]) -> sg.TabGroup:
    person_layout = []
    for i, person in enumerate(individual):
        section_key = f'-SECTION{i}-'
        pending_action_layout = [[sg.Text("PendingAction:")], [sg.Listbox(values=person.get_pending_action_as_list(), size=(30, 7),  horizontal_scroll= True, key=f'-PENDINGACTION{i}-')]]
        obey_subject_layout = [[sg.Text("ObeySubject:")], [sg.Listbox(values = person.obey_stats.subject, size=(30, 5),  horizontal_scroll= True, key=f'-OBEYSUBJECT{i}-')]]
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
                   ]
        right_section = [[sg.Column(pending_action_layout)],
                        [sg.Column(obey_subject_layout)]
                        ]
        section = [[sg.Column(left_section), sg.Column(right_section)]]
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
    special_log_layout = [[sg.Output(size=(80,15), key='-SPECIAL OUTPUT-')]]
    layout_left = person_layout + special_log_layout
    console_log_layout = [[sg.Output(size=(80,30), key='-OUTPUT-')]]
    button_layout = [[sg.Button('Start', key= '-START-'), sg.Button('Stop', key= '-STOP-'), sg.Button('Clear', key= '-Clear-'), sg.Button('Exit', key= '-Exit-') ,sg.Button('Export', key= '-Export-')]]
    layout_right = console_log_layout+ button_layout
    #column layout of person_layout and console_log_layout
    layout = [[sg.Column(layout_left), sg.Column(layout_right)]]
    window = sg.Window('LLM Social Simulation', layout)
    thread: threading.Thread
    system.set_console_log(CustomConsoleLog(window, '-SPECIAL OUTPUT-'))
    isappStarted = False
        # Redirect stdout to the sg.Output element
    while True:             # Event Loop
        event, values = window.read(timeout=100) #update every 100ms
        if event == sg.WIN_CLOSED:
            break
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
            thread = window.start_thread(lambda: start_simulate(system), ('-THREAD-', '-THEAD ENDED-'))
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
           
        
        #update 
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
            
            # Update Listbox, Remain the listbox scroll position
            for key in [f'-PENDINGACTION{i}-', f'-OBEYSUBJECT{i}-']:
                # Access the tkinter Listbox widget
                lb_widget = window[key].Widget

                # Get current scroll position
                scroll_position = lb_widget.yview()

                if key == f'-PENDINGACTION{i}-':
                    new_values = person.get_pending_action_as_list()
                else: # key == f'-OBEYSUBJECT{i}-':
                    new_values = person.obey_stats.subject
                
                window[key].update(new_values)
            
                # Set the scroll position to the previous position
                lb_widget.yview_moveto(scroll_position[0])
            
        window.refresh()
            

    window.close()

if __name__ == "__main__":
    main()
