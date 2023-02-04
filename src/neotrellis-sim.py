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

if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# Global constants which define the size, separation and number of buttons on
# the simulated NeoTrellis hardware
BTN_MARGIN = 10
BTN_SIZE = 30
DIM_X = 12
DIM_Y = 12

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

# Audio player class which mimics the interface of the audiocore class from Circuit Python
# Allows code to play sounds in Circuit Python to play the sounds in Pygame in the simulator
class AudioPlayer:
    def play(self,sound):
        sound.getSound().play()

# Track long single button presses to use to over-ride game classes
lastBtnPressed = [-1,-1]
lastPressTime = 0
longPressInterval = 1000000000

## Main simulator method
def main():
    global activeGame
    
    audio = AudioPlayer()

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
            #pygame.display.update()
            #print(f"At {x},{y}: {colour}")
        else:
            print(f"Request to set colour outside trellis at: {x},{y}")

    def getColour(x,y):
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
        
        print(f"Button long press at {x},{y}")
        if y == 11:
            if x == 0:
                gridReset((50,0,50))
                activeGame = BtnDemo(getColour, setColour, audio)
            elif x == 1:
                # gridReset((10,10,10))
                activeGame = Battleships(getColour, setColour)
            elif x == 11:
                gridReset((0,0,0))
                activeGame = RainDemo(getColour, setColour)

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
                      
    activeGame = Battleships(getColour, setColour)

    ## Simulation loop ##
    while running:
        # Process pygame events
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
            #print(f"Long press activated for position {lastBtnPressed[0]},{lastBtnPressed[1]}")
            setColour(lastBtnPressed[0], lastBtnPressed[1], (255, 80, 0), False )
            
        pygame.display.update()
        time.sleep(0.02)

        
    main()

print("Running")
if __name__ == '__main__':
    main()
    
