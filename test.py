import PySimpleGUI as sg
import time

# Sample initial data for the list box
data = ['Item 1', 'Item 2', 'Item 3']

layout = [
    [sg.Listbox(values=data, size=(20, 4), key='-LISTBOX-')],
    [sg.Button('Start Updating'), sg.Button('Stop Updating'), sg.Button('Exit')]
]

window = sg.Window('Update Listbox Each Frame', layout)

updating = False
counter = 0

while True:
    event, values = window.read(timeout=100)  # timeout in milliseconds

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Start Updating':
        updating = True
    elif event == 'Stop Updating':
        updating = False

    print("a")

window.close()
