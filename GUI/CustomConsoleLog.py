import PySimpleGUI as sg
class CustomConsoleLog:
    def __init__(self, window:sg.Window, key:str):
        self.key = key
        self.window = window
        self.content = ''
    def append(self, message):
        # Retrieve the current content
        current_content = self.window[self.key].get()
        
        # Append the new message
        self.content = current_content + message
    #all update should be done in main thread to avoid conflict