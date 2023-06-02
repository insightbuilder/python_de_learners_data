#Script adds the buttons

import PySimpleGUI as sg

layout = [[sg.Text("Hello from PSG")],
          [sg.Button("OK")]]

#Work on the window

win = sg.Window("New Demo",
                layout)

#This loop checks for the events
while True:
    event, values = win.read()

    if event == 'OK' or event == sg.WIN_CLOSED:
        print(event)
        break

win.close()


