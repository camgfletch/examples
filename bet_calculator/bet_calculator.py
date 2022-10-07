#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PySimpleGUI as sg
sg.theme('BluePurple')

layout = [[sg.Text('Enter fund*:'), sg.Text(size=(15,1))],
          [sg.Input(key='fund')],
          [sg.Text('Enter odds*:'), sg.Text(size=(15,1))],
          [sg.Input(key='odds')],
          [sg.Text('Model probability (percentage chance e.g. 70)*:'), sg.Text(size=(15,1))],
          [sg.Input(key='prob')],
          [sg.Text('Bet size (auto):'), sg.Text(size=(15,1))],
          [sg.Input(key='betsize')],
          [sg.Text('Bet value (auto):'), sg.Text(size=(15,1))],
          [sg.Input(key='betvalue')],
          [sg.Text('Bet payout (auto):'), sg.Text(size=(15,1))],
          [sg.Input(key='payout')],
          [sg.Button('Calculate'), sg.Button('Exit')]]

window = sg.Window('Bet Calculator', layout)
  
    
while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Calculate':
        # Saved inputs
        fund = float(values['fund'])
        odds = float(values['odds'])
        prob = float(values['prob'])
        # Background info & basic calculations
        stake = fund * 0.04
        betsize = stake / odds
        betsize = round(betsize, 2)
        # Bet value calculations
        betvalue = 1 / odds * 100
        betvalue = prob - betvalue
        betvalue = round(betvalue, 2)
        payout = (betsize * odds) - betsize
        payout = round(payout, 2)
        
        # Update cell input
        window['betsize'].update(betsize)
        window['betvalue'].update(betvalue)
        window['payout'].update(payout)

window.close()

