# SPDX-FileCopyrightText: 2022 Dr Footleg
# SPDX-License-Identifier: GPLv3

"""
Neotrellis multi board matrix game host program.
Hosts a series of game classes which each implement a btnEvent method which this host
program calls on each button press or release on the Trellis matrix to notify the game that a
button event has occurred. Each game class is also passed a getColour and setColour method in
the constructor to provide a means to read or set the colours of the LEDs behind the buttons.
All other logic is then implemented in the game classes using these 3 methods (plus sound playing
methods still WIP).

The host program holds a reference to the active game class instance in the variable 'activeGame'.
Long button press events (press and hold for 3 seconds) are handled by the host program and used
to swap between different games.
"""

import time
import board
import busio
import microcontroller
import audiobusio
from audiocore import WaveFile
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis
from digitalio import DigitalInOut, Direction, Pull

from btn_demo import BtnDemo
from rain_demo import RainDemo
from TrellisBattleships import Battleships

bootBtn = DigitalInOut(microcontroller.pin.GPIO23)
bootBtn.direction = Direction.INPUT

audio = audiobusio.I2SOut(board.GP1, board.GP2, board.GP3)

# Create the I2C object for the NeoTrellis
i2c_bus = busio.I2C(scl=board.GP5, sda=board.GP4)

# Create the NeoTrellis object
# This is for a 3x3 array of NeoTrellis boards:
trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x36), NeoTrellis(i2c_bus, False, addr=0x37), NeoTrellis(i2c_bus, False, addr=0x38)],
    [NeoTrellis(i2c_bus, False, addr=0x32), NeoTrellis(i2c_bus, False, addr=0x33), NeoTrellis(i2c_bus, False, addr=0x34)],
    [NeoTrellis(i2c_bus, False, addr=0x2E), NeoTrellis(i2c_bus, False, addr=0x2F), NeoTrellis(i2c_bus, False, addr=0x30)],
]
dimY = 12
dimX = 12

trellis = MultiTrellis(trelli)

"""
Host class: Holds references to all the trellis hardware capabilities and a dictionary of sound samples.
All applications running on the matrix are passed a reference to the host object and access the LEDs
through the host for getting and setting colours, and to play sounds. This architecture simplifies the
application code and also enables a digital twin to run the same application classes in a software 
simulation of the hardware.
"""
class Host:
    def __init__(self,getColour,setColour,audio):
        self.getColour = getColour
        self.setColour = setColour
        self.audio = audio

        print("Loading sound files into memory")
        self.sounds_dict = {}

        # Load sound files into sounds dictionary
        self.sounds_dict['glass_break'] = WaveFile(open("./sounds/GlassBreak.wav", "rb"))
        # Load sound files with text keys to identify them here (just a few CC licensed sound files are included in source as examples)
        # self.sounds_dict['sound_key'] = WaveFile(open("./sounds/soundfile.wav", "rb"))

    def getColour(self):
        return self.getColour

    def setColour(self):
        return self.setColour

    def restoreColour(self,x,y):
        self.setColour(x,y,self.getColour(x,y),False)

    def play(self,key):
        try:
            self.audio.play(self.sounds_dict[key])
        except(KeyError):
            print(f"No sound matching key: {key}")


# Track long single button presses to use to over-ride game classes
lastBtnPressed = [-1,-1]
lastPressTime = 0
longPressInterval = 1000000000

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.1

# some color definitions
leds = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0],
        ]


def setColour(x,y,colour,store=True):
    if 0 <= x <= 11 and 0 <= y <= 11:
        if store:
            leds[y * dimY + x] = colour
        trellis.color(x, y, colour)
        #print(f"At {x},{y}: {colour}")
    else:
        print(f"Request to set colour outside trellis at: {x},{y}")


def getColour(x,y):
    return leds[y * dimY + x]


def gridReset(colour):
    """
    Resets all lights and stored colours to the same colour value
    """
    for y in range(dimY):
        for x in range(dimX):
            setColour( x, y, colour )


def longPress(x,y):
    global activeGame
    
    print(f"Button long press at {x},{y}")
    if y == 0:
        if x == 6:
            trellis.brightness = 0.1
        elif x == 7:
            trellis.brightness = 0.2
        elif x == 8:
            trellis.brightness = 0.4
        elif x == 9:
            trellis.brightness = 0.6
        elif x == 10:
            trellis.brightness = 0.8
        elif x == 11:
            trellis.brightness = 1.0
        else:
            # Pass unhandled long press events to active game
            activeGame.longPressEvent(x,y)
    elif y == 11:
        if x == 0:
            gridReset((50,0,50))
            activeGame = BtnDemo(host)
        elif x == 1:
            # gridReset((10,10,10))
            activeGame = Battleships(host)
        elif x == 11:
            gridReset((0,0,0))
            activeGame = RainDemo(host)
        else:
            # Pass unhandled long press events to active game
            activeGame.longPressEvent(x,y)
    else:
        # Pass unhandled long press events to active game
        activeGame.longPressEvent(x,y)

    # Restore button colour
    host.restoreColour(x,y)


# this will be called when button events are received
def btnHandler(x, y, edge):
    global lastBtnPressed, lastPressTime
    
    #print(f"Button pressed {x},{y}")
    # Check for button pressed and released events, and pass to active game class
    if edge == NeoTrellis.EDGE_RISING:
        # Store position of button for checking for long press events
        lastBtnPressed = [x,y]
        # Call active game class button event handler
        activeGame.btnEvent(x,y,True)
    elif edge == NeoTrellis.EDGE_FALLING:
        # Check for long button press
        if (lastBtnPressed == [x,y]) and ((time.monotonic_ns() - lastPressTime) > longPressInterval):
            # Long press
            setColour(x, y, (0,0,0), False)
            longPress(x, y)

    # Call active game class button event handler
        activeGame.btnEvent(x,y,False)
        # Clear last pressed position on any button release
        lastBtnPressed = [-1,-1]
    
    # Reset last press time on any button event
    lastPressTime = time.monotonic_ns()
        
        
for y in range(dimY):
    for x in range(dimX):
        # Activate rising edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        # Activate falling edge events on all keys
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, btnHandler)
        trellis.color( x, y, (100, 0, 255) )

host = Host(getColour,setColour,audio)

activeGame = Battleships(host)

while True:
    # The NeoTrellis can only be read every 17 milliseconds or so
    trellis.sync()
    activeGame.animate()

    if (lastBtnPressed[0] >= 0) and ((time.monotonic_ns() - lastPressTime) > longPressInterval):
        #Long press will be activated when key is lifted, so indicate with colour change
        #print(f"Long press activated for position {lastBtnPressed[0]},{lastBtnPressed[1]}")
        setColour(lastBtnPressed[0], lastBtnPressed[1], (255, 80, 0), False )

    if bootBtn.value == False:
        print("Boot button pressed.")
        
    time.sleep(0.02)

