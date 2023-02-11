# Neotrellis Simulator - A virtual twin of a 12 x 12 button neotrellis
# Copyright (C) 2023 Paul 'Footleg' Fretwell

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame, os, platform, random, sys
import time

from btn_demo import BtnDemo
from rain_demo import RainDemo
from trellisbattleships import Battleships

### Mock Circuit Python audio classes
class WaveFile:
    def __init__(self, wave_file):
        self.wav = wave_file

    def getSound(self):
        return self.wav

# Override file open command for simulator so that we return a pygame sound rather than the 
# IO buffer that the Python open() method normally returns (which the Circuit Python audio code player uses).
def open(filepath,readmode):
    return pygame.mixer.Sound(filepath) 


if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# Global constants which define the size, separation and number of buttons on
# the simulated NeoTrellis hardware
BTN_MARGIN = 10
BTN_SIZE = 30
DIM_X = 12
DIM_Y = 12

RED = (255, 0, 0)
ORANGE = (255, 100, 0)

# Define the window size based on the constants defined above
SCR_SIZE = SCR_W, SCR_H = BTN_MARGIN + (BTN_MARGIN + BTN_SIZE) * DIM_X, BTN_MARGIN + (BTN_MARGIN + BTN_SIZE) * DIM_Y

def exit_game():
    pygame.quit()
    sys.exit()

# Virtual hardware class definition
class MultiTrellis:
    def __init__(self,screen):
        self.screen = screen

    def color(self, x, y, colour):
        # Draw button rectangle
        pygame.draw.rect(self.screen,colour,(BTN_MARGIN + x * (BTN_MARGIN + BTN_SIZE),BTN_MARGIN + y * (BTN_MARGIN + BTN_SIZE),BTN_SIZE,BTN_SIZE))

"""
Host class: Holds references to all the trellis hardware capabilities and a dictionary of sound samples.
All applications running on the matrix are passed a reference to the host object and access the LEDs
through the host for getting and setting colours, and to play sounds. This architecture simplifies the
application code and also enables a digital twin to run the same application classes in a software 
simulation of the hardware.
"""
class Host:
    def __init__(self,getColour,setColour):
        self.getColour = getColour
        self.setColour = setColour

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
            self.sounds_dict[key].getSound().play()
            print(f"Playing sound: {key}")
        except(KeyError):
            print(f"No sound matching key: {key}")


# Track long single button presses to use to over-ride game classes
lastBtnPressed = [-1,-1]
lastPressTime = 0
longPressInterval = 1000000000

# Track time since last hardware sync, so we give at a least 17ms pause between sync requests
lastSyncTime = 0

## Main simulator method
def main():
    global activeGame, lastSyncTime

    pygame.init()
    screen = pygame.display.set_mode(SCR_SIZE)    
    pygame.display.set_caption("Neotrellis Simulator")
    screen_rect = screen.get_rect()
    running = True

    # Create the virtual neotrellis with a reference to the pygame drawing surface to render itself
    trellis = MultiTrellis(screen)

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
                leds[y * DIM_Y + x] = colour
            trellis.color(x, y, colour)
            pygame.display.update()
            time.sleep(0.001)
        else:
            print(f"Request to set colour outside trellis at: {x},{y}")

    def getColour(x,y):
        time.sleep(0.01)
        return leds[y * DIM_Y + x]

    def gridReset(colour):
        """
        Resets all lights and stored colours to the same colour value
        """
        for y in range(DIM_Y):
            for x in range(DIM_X):
                setColour( x, y, colour )
        
    def longPress(x,y):
        global activeGame
        
        print(f"Button long press at {x},{y} (was colour: {getColour(x,y)})")
        if y == 11:
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

        # Restore button colour
        host.restoreColour(x,y)

    # this will be called when button events are received
    def btnHandler(x, y, edge):
        global lastBtnPressed, lastPressTime
        
        print(f"Button pressed {x},{y}")
        # Check for button pressed and released events, and pass to active game class
        if edge == True:
            # Store position of button for checking for long press events
            lastBtnPressed = [x,y]
            # Call active game class button event handler
            activeGame.btnEvent(x,y,True)
        elif edge == False:
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

    host = Host(getColour,setColour)
    
    # Set the game to load automatically on boot
    activeGame = Battleships(host)

    ## Simulation loop ##
    while running:
        timenow = time.monotonic_ns()
        if timenow - lastSyncTime > 18000:
            lastSyncTime = timenow
            # Mock of Trellis sync: Process pygame events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        xPos = int((pygame.mouse.get_pos()[0] - BTN_MARGIN) / (BTN_SIZE + BTN_MARGIN))
                        yPos = int((pygame.mouse.get_pos()[1] - BTN_MARGIN) / (BTN_SIZE + BTN_MARGIN))
                        btnHandler( xPos, yPos, event.type == pygame.MOUSEBUTTONDOWN )
                elif event.type == pygame.QUIT:
                    exit_game()

            # Check for key presses (ESC to exit simulator)
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                exit_game()

            activeGame.animate()

            if (lastBtnPressed[0] >= 0) and ((time.monotonic_ns() - lastPressTime) > longPressInterval):
                #Long press will be activated when key is lifted, so indicate with colour change
                longPressColour = RED
                #Use a different colour to the one this button is currently showing
                colourNow = getColour(lastBtnPressed[0], lastBtnPressed[1])
                if colourNow == RED:
                    longPressColour = ORANGE
                #print(f"Long press activated for position {lastBtnPressed[0]},{lastBtnPressed[1]}")
                setColour(lastBtnPressed[0], lastBtnPressed[1], longPressColour, False )
                
            pygame.display.update()

        time.sleep(0.002)
        
    main()

print("Running")
if __name__ == '__main__':
    main()
    
