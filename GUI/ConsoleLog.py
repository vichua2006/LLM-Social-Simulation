import PySimpleGUI as sg
class ConsoleLog: 
    def __init__(self, window:sg.Window, key):
        self.window = window
        self.key = key

    def write(self, string):
        #Thread Safe
        self.window.write_event_value(self.key, string)

    def flush(self):
        pass