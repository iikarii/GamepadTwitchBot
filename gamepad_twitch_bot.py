#MIT License

#Copyright (c) 2024 iikarii

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import os
import asyncio
import vgamepad as vg
from twitchio.ext import commands

#TODO: set your own TWITCH_TOKEN and INITIAL_CHANNELS variables
TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
INITIAL_CHANNELS = ['AuskaAI']

class Gamepad_Twitch_Bot(commands.Bot):
    """
    A Twitch bot that maps chat commands to gamepad inputs.
    """

    #Variables
    pull  = 255 #pull strength 1-255
    hold  = 0.2 #seconds press time
    delay = 0.1 #seconds delay after input

    #Class Attributes (Controller Maps)
    GAMEPAD = vg.VX360Gamepad()
    KEYS = [
        'w','a','s','d', #left stick
        'W','A','S','D', #right stick
        '1','2','3','4', #d-pad
        'f','c','r','g', #ABXY
        'q','e','R','F', #shoulders/triggers
        'Q','E','x','z', #thumbs/start/select
    ]
    BUTTON_DICT = {
    '1': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    '2': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    '3': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    '4': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    'f': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'c': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'r': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'g': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    'q': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'e': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    'Q': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    'E': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    'z': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    }

    STICK_DICT = {
    'w': ('L',  0,  1),
    'a': ('L', -1,  0),
    's': ('L',  0, -1),
    'd': ('L',  1,  0),
    'W': ('R',  0,  1),
    'A': ('R', -1,  0),
    'S': ('R',  0, -1),
    'D': ('R',  1,  0),
    }

    TRIGGER_DICT = {
    'R': ('L', pull),
    'F': ('R', pull),
    }

    #TwitchIO Functions
    def __init__(self):
        try: super().__init__(token=TWITCH_TOKEN, prefix='!', initial_channels=INITIAL_CHANNELS)
        except Exception as e: print(f"Error: {e}\n Did you forget to set TWITCH_TOKEN and INITIAL_CHANNELS?")

    async def event_ready(self): print(f'Logged in as | {self.nick}'); print(f'User id is | {self.user_id}\n')

    async def event_message(self, message): 
        if all(key in self.KEYS for key in message.content):
            for key in message.content: await self.gamepad_input(key); await asyncio.sleep(self.delay)

    #Input Functions
    async def gamepad_input(self,key):
        if key in self.BUTTON_DICT: await self.button_input(*self.BUTTON_DICT[key])
        if key in self.STICK_DICT: await self.stick_input(*self.STICK_DICT[key])
        if key in self.TRIGGER_DICT: await self.trigger_input(*self.TRIGGER_DICT[key])

    async def button_input(self,button):
        self.GAMEPAD.press_button(button); self.GAMEPAD.update()    
        await asyncio.sleep(self.hold)                               
        self.GAMEPAD.release_button(button); self.GAMEPAD.update()   

    async def stick_input(self,side,x,y):
        if side == 'L': self.GAMEPAD.left_joystick_float(x,y) 
        else: self.GAMEPAD.right_joystick_float(x,y)
        self.GAMEPAD.update(); await asyncio.sleep(self.hold)                               
        self.GAMEPAD.left_joystick_float(0,0); self.GAMEPAD.right_joystick_float(0,0); self.GAMEPAD.update() 

    async def trigger_input(self,side,value):
        if side == 'L': self.GAMEPAD.left_trigger(value)
        else: self.GAMEPAD.right_trigger(value)
        self.GAMEPAD.update(); await asyncio.sleep(self.hold)                          
        self.GAMEPAD.left_trigger(0); self.GAMEPAD.right_trigger(0); self.GAMEPAD.update() 

Gamepad_Twitch_Bot().run()
