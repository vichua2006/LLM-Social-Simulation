import PySimpleGUI as sg
class CustomConsoleLog:
    def __init__(self, window:sg.Window, key:str):
        self.key = key
        self.window = window

    def append(self, message):
        # Retrieve the current content
        current_content = self.window[self.key].get()
        
        # Append the new message
        updated_content = current_content + message + '\n'
        
        # Update the Output element with the new content
        self.window[self.key].update(updated_content)