import PySimpleGUI as sg
class ConsoleLog: 
    def __init__(self, window:sg.Window, key, thread_key):
        self.window = window
        self.key = key
        self.thread_key = thread_key

    def write(self, string):
        #Thread Safe
        self.window.write_event_value(self.thread_key, string)

    def flush(self):
        pass