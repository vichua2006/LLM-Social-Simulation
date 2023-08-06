import threading
import PySimpleGUI as sg
from typing import List, Tuple
from Main.Individual import Individual, System
from Main.Simulation import initialize, simulate

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
                   
                   ]
        person_layout.append(sg.Tab(f'Person {i+1}', section, key=section_key))
    return sg.TabGroup([person_layout], size=(200, 200))


def start_simulate(system:System, stop_event: threading.Event):
    for i in range(2):
        simulate(system.individuals, system, stop_event)
def main():
    isappStarted = False
    system=initialize()
    individuals = system.individuals
    person_layout = create_individual_layout(individuals)
    console_log = [[sg.Output(size=(80,30), key='-OUTPUT-')]] 
    button:List[List[button]] = [[sg.Button('Start', key= '-START-')], [sg.Button('Stop', key= '-STOP-')], [sg.Button('Clear', key= '-Clear-')], [sg.Button('Exit', key= '-Exit-')]]
    layout = [[person_layout], [console_log], button]

    window = sg.Window('LLM Social Simulation', layout)
        # Redirect stdout to the sg.Output element
    while True:             # Event Loop
        event, values = window.read()
        thread: threading.Thread
        stop_event_flag = threading.Event()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-Clear-':
            window['-OUTPUT-'].update('')
        elif event == '-Exit-':
            break
        elif event == '-START-':
            print("Start")
            stop_event_flag.clear()
            thread = window.start_thread(lambda: start_simulate(system, stop_event_flag), ('-THREAD-', '-THEAD ENDED-'))
            isappStarted = True
        elif event == '-STOP-':
            print("Stop")
            stop_event_flag.set()
            isappStarted = False
            
        # Check if event is a section Collapsible
        if '-COLLASPSIBLE-' in event:
            section_key = event.split('-COLLASPSIBLE-')[0]
            window[section_key].update(visible=not window[section_key].visible)
            window[section_key+'-COLLASPSIBLE-'].update(window[section_key].metadata[0] if window[section_key].visible else window[section_key].metadata[1])

    window.close()

if __name__ == "__main__":
    main()
