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

class Gamepad_Twitch_Bot(commands.Bot):

    #Class Attributes
    gamepad        = vg.VX360Gamepad()
    trigger_value  = 255 #pull strength
    hold_duration  = 0.2 #button press time
    delay_duration = 0.1 #delay between inputs

    #Controller Maps
    keys = [
        'w','a','s','d', #left stick
        'W','A','S','D', #right stick
        '1','2','3','4', #d-pad
        'f','c','r','g', #ABXY
        'q','e','R','F', #shoulders/triggers
        'Q','E','x','z', #thumbs/start/select
    ]

    key_button_dict = {
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

    key_stick_dict = {
    'w': ('left',   0,  1),
    'a': ('left',  -1,  0),
    's': ('left',   0, -1),
    'd': ('left',   1,  0),
    'W': ('right',  0,  1),
    'A': ('right', -1,  0),
    'S': ('right',  0, -1),
    'D': ('right',  1,  0),
    }

    key_trigger_dict = {
    'R': ('left',  trigger_value),
    'F': ('right', trigger_value),
    }

    #TwitchIO Functions
    def __init__(self): 
        super().__init__(token=os.environ['TWITCH_TOKEN'], prefix='!', initial_channels=['AuskaAI'])

    async def event_ready(self): 
        print(f'Logged in as | {self.nick}'); print(f'User id is | {self.user_id}\n')

    async def event_message(self, message): 
        if all(key in self.keys for key in message.content):
            for key in message.content: await self.gamepad_input(key); await asyncio.sleep(self.delay_duration)

    #Input Functions
    async def gamepad_input(self,key):
        if key in self.key_button_dict:  await self.button_input(*self.key_button_dict[key])
        if key in self.key_stick_dict:   await self.stick_input(*self.key_stick_dict[key])
        if key in self.key_trigger_dict: await self.trigger_input(*self.key_trigger_dict[key])

    async def button_input(self,button):
        self.gamepad.press_button(button);   self.gamepad.update()    
        await asyncio.sleep(self.hold_duration)                               
        self.gamepad.release_button(button); self.gamepad.update()   

    async def stick_input(self,side,x,y):
        if side == 'right':
            self.gamepad.right_joystick_float(x,y); self.gamepad.update() 
            await asyncio.sleep(self.hold_duration)                               
            self.gamepad.right_joystick_float(0,0); self.gamepad.update() 
        elif side == 'left':
            self.gamepad.left_joystick_float(x,y);  self.gamepad.update() 
            await asyncio.sleep(self.hold_duration)                           
            self.gamepad.left_joystick_float(0,0);  self.gamepad.update() 

    async def trigger_input(self,side,value):
        if side == 'right':
            self.gamepad.right_trigger(value); self.gamepad.update() 
            await asyncio.sleep(self.hold_duration)                          
            self.gamepad.right_trigger(0);     self.gamepad.update() 

        elif side == 'left':
            self.gamepad.left_trigger(value);  self.gamepad.update()  
            await asyncio.sleep(self.hold_duration)                          
            self.gamepad.left_trigger(0);      self.gamepad.update()  

Gamepad_Twitch_Bot().run()