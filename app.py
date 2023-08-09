import threading
import PySimpleGUI as sg
from typing import List, Tuple
from Main.Individual import Individual, System
from Main.Simulation import initialize, simulate
import time

def create_individual_layout(individual: List[Individual]) -> sg.TabGroup:
    person_layout = []
    for i, person in enumerate(individual):
        section_key = f'-SECTION{i}-'
        section = [[sg.Text('Aggressiveness:'), sg.Input(person.attributes["aggressiveness"], key=f'-AGGRESSIVENESS{i}-')],
                   [sg.Text('Covetousness:'), sg.Input(person.attributes["covetousness"], key=f'-COVETOUSNESS{i}-')],
                   [sg.Text('Intelligence:'), sg.Input(person.attributes["intelligence"], key=f'-INTELLIGENCE{i}-')],
                   [sg.Text('Strength:'), sg.Input(person.attributes["strength"], key=f'-STRENGTH{i}-')],
                   [sg.Text('SocialPosition:'), sg.Input(person.attributes["social_position"], key=f'-SOCIALPOSITION{i}-')],
                   [sg.Text('Food:'), sg.Input(person.attributes["food"], key=f'-FOOD{i}-')],
                   [sg.Text('Land:'), sg.Input(person.attributes["land"], key=f'-LAND{i}-')],
                   [sg.Text('CurrentActionType:'), sg.Input(person.current_action_type, key=f'-CURRENTACTIONTYPE{i}-')],
                   [sg.Listbox(values=person.get_pending_action_as_list(), size=(100, 200),  horizontal_scroll= True, key=f'-PENDINGACTION{i}-')]
                   ]
        person_layout.append(sg.Tab(f'Person {i}', section, key=section_key))
    return sg.TabGroup([person_layout], size=(200, 300))


def start_simulate(system:System):
    for i in range(2):
        simulate(system.individuals, system)
def main():

    system=initialize()
    individuals = system.individuals
    person_layout = create_individual_layout(individuals)
    console_log = [[sg.Output(size=(80,30), key='-OUTPUT-')]] 
    button:List[List[button]] = [[sg.Button('Start', key= '-START-')], [sg.Button('Stop', key= '-STOP-')], [sg.Button('Clear', key= '-Clear-')], [sg.Button('Exit', key= '-Exit-')]]
    layout = [[person_layout], [console_log], button]
    isappStarted = False
    window = sg.Window('LLM Social Simulation', layout)
    thread: threading.Thread
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
        
        #update 
        for i, person in enumerate(individuals):
            window[f'-AGGRESSIVENESS{i}-'].update(person.attributes["aggressiveness"])
            window[f'-COVETOUSNESS{i}-'].update(person.attributes["covetousness"])
            window[f'-INTELLIGENCE{i}-'].update(person.attributes["intelligence"])
            window[f'-STRENGTH{i}-'].update(person.attributes["strength"])
            window[f'-SOCIALPOSITION{i}-'].update(person.attributes["social_position"])
            window[f'-FOOD{i}-'].update(person.attributes["food"])
            window[f'-LAND{i}-'].update(person.attributes["land"])
            window[f'-CURRENTACTIONTYPE{i}-'].update(person.current_action_type)
            window[f'-PENDINGACTION{i}-'].update(person.get_pending_action_as_list())
       
            

    window.close()

if __name__ == "__main__":
    main()
