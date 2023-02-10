# Ship find and destroy game demo for the Neotrellis Matrix

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

import random
import time

OFF = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 120, 0)
YELLOW = (255, 180, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
PURPLE = (100, 0, 255)
WHITE = (255,255,255)
DIMWHITE = (20,20,20)

MISS = BLUE
HIT = RED
NOTTRIED = DIMWHITE

TURNTIME = 2200000000
ANIMATEINTERVAL = 330000000
MAXSHOTS = 44

"""
No. Class of ship Size
1   Carrier        5
2   Battleship     4
3   Cruiser        3
4   Submarine      3
5   Destroyer      2
"""

class Battleships:
    def __init__(self, host):
        # Host contains all the RGB LED access and audio play methods of the hardware
        self.host = host

        self.enableBtns = False
        self.audioVolume = 1
        self.flipflop = False
        self.maxTries = MAXSHOTS
        
        self.startGame()


    def startGame(self):
        self.enableBtns = False

        # Initialise game variables
        self.btnDown = False
        self.activeBtn = (-1,-1)
        self.turnStarted = 0 #0 indication no turn active, otherwise the time the turn started is stored
        self.gamestage = 0 # 0=waiting for player to take shot; 1=shot fired; 2=ship hit; 3=ship sinking, 4=game over
        self.misses = 0
        self.remainingships = 5

        # Create ships
        self.carrier = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.battleship = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.cruiser = [[0,0,0],[0,0,0],[0,0,0]]
        self.submarine = [[0,0,0],[0,0,0],[0,0,0]]
        self.destroyer = [[0,0,0],[0,0,0]]

        # Draw border
        for x in range(12):
            self.host.setColour( x, 0, GREEN )
            self.host.setColour( x, 11, GREEN )
        for y in range(12):
            self.host.setColour( 0, y, GREEN )
            self.host.setColour( 11, y, GREEN )

        # Draw playing area
        for y in range(1,11):
            for x in range(1,11):
                self.host.setColour( x, y, NOTTRIED )

        # Place ships
        self.placeShip(self.carrier)
        self.placeShip(self.battleship)
        self.placeShip(self.cruiser)
        self.placeShip(self.submarine)
        self.placeShip(self.destroyer)

        # Allow player to start taking shots
        self.enableBtns = True


    def btnEvent(self, x, y, press):
        if self.enableBtns:
            if press:
                # Only allow one button to be down at a time
                if self.btnDown == False:
                    # Check if a valid button selection for the game
                    if 0 < x < 11 and 0 < y < 11 and self.host.getColour(x,y) == NOTTRIED:
                        self.btnDown = True
                        self.activeBtn = (x,y)
                        self.host.setColour(x,y,WHITE,False)
            else:
                # Only act on release of the active button
                if x == self.activeBtn[0] and y == self.activeBtn[1]:
                    self.enableBtns = False
                    self.btnDown = False
                    # Take turn if at turn taking game stage
                    if self.gamestage == 0:
                        self.turnStarted = time.monotonic_ns()
                        self.animatetime = self.turnStarted - ANIMATEINTERVAL # Set to time out immediately
                        self.gamestage = 1
                        if self.audioVolume == 1:
                            self.host.play('QuickBombDrop_1')
                        elif self.audioVolume == 2:
                            self.host.play('QuickBombDrop_2')
                        elif self.audioVolume == 3:
                            self.host.play('QuickBombDrop_3')
                        elif self.audioVolume == 4:
                            self.host.play('QuickBombDrop_4')
                    

    def longPressEvent(self, x, y):
        if y == 0:
            if x < 5:
                self.audioVolume = x
                print(f"Audio Volume: {self.audioVolume}")
        elif y == 1:
            if x < 4 and self.misses == 0:
                # Reset game difficulty if at start of game
                self.maxTries = 11 + x * 11
                for idx in range(self.maxTries):
                    self.misses = idx + 1
                    self.updateScore(RED)
                    time.sleep(0.05)
                time.sleep(0.5)
                # Trigger end of game to restart
                self.endGame()


    def animate(self):
        # Increment animations which run independent of button presses
        if self.activeBtn != (-1,-1) and self.gamestage == 1:
            # Animate shot incoming
            timenow = time.monotonic_ns()
            # Active turn
            #print(f"turn active started at {self.turnStarted} animatetime {self.animatetime} timenow {timenow}")
            if timenow - self.turnStarted > TURNTIME:
                print(f"turn started at {self.turnStarted} ended at {timenow}")
                # Shot landed, determine outcome
                outcome = self.takeShot(self.activeBtn[0],self.activeBtn[1]) 
                if outcome == 0:
                    # Shot missed
                    self.misses += 1
                    self.updateScore()
                    self.host.setColour(self.activeBtn[0],self.activeBtn[1],BLUE)
                    if self.audioVolume == 1:
                        self.host.play('WaterSplash_1')
                    elif self.audioVolume == 2:
                        self.host.play('WaterSplash_2')
                    elif self.audioVolume == 3:
                        self.host.play('WaterSplash_3')
                    elif self.audioVolume == 4:
                        self.host.play('WaterSplash_4')
                    if self.misses >= self.maxTries:
                        # Game over, out of ammo
                        self.endGame()
                    else:
                        self.endTurn()
                else:
                    self.gamestage = outcome + 1
                    if self.gamestage == 3:
                        # Play ship sunk sound (animate loop will show sinking with LEDs)
                        if self.audioVolume == 1:
                            self.host.play('EpicExplosion_1')
                        elif self.audioVolume == 2:
                            self.host.play('EpicExplosion_2')
                        elif self.audioVolume == 3:
                            self.host.play('EpicExplosion_3')
                        elif self.audioVolume == 4:
                            self.host.play('EpicExplosion_4')
                        # Reset timers for animation of ship sinking
                        self.turnStarted = time.monotonic_ns()
                        self.animatetime = self.turnStarted - ANIMATEINTERVAL # Set to time out immediately
            elif timenow - self.animatetime > ANIMATEINTERVAL:
                print("turn animating")
                self.animatetime = time.monotonic_ns()
                # Flash button
                if self.host.getColour(self.activeBtn[0],self.activeBtn[1]) != YELLOW:
                    self.host.setColour(self.activeBtn[0],self.activeBtn[1],YELLOW)
                else:
                    self.host.setColour(self.activeBtn[0],self.activeBtn[1],NOTTRIED)
        elif self.gamestage == 2:
            # Ship hit
            self.host.setColour(self.activeBtn[0],self.activeBtn[1],ORANGE)
            if self.audioVolume == 1:
                self.host.play('SeaMineExplosion_1')
            elif self.audioVolume == 2:
                self.host.play('SeaMineExplosion_2')
            elif self.audioVolume == 3:
                self.host.play('SeaMineExplosion_3')
            elif self.audioVolume == 4:
                self.host.play('SeaMineExplosion_4')
            self.endTurn()
        elif self.gamestage == 3:
            # Animate ship sinking
            timenow = time.monotonic_ns()
            if timenow - self.turnStarted > TURNTIME * 1.5:
                # Ship sunk
                self.drawShip(self.activeShip,YELLOW,RED)
                self.remainingships += -1
                if self.remainingships > 0:
                    self.endTurn()
                else:
                    # Game won
                    self.endGame()
            elif timenow - self.animatetime > ANIMATEINTERVAL:
                print("sinking animation")
                for pos in self.activeShip:
                    rnd = random.randint(0,2)
                    if rnd == 0:
                        self.host.setColour(pos[0],pos[1],YELLOW)
                    elif rnd == 1:
                        self.host.setColour(pos[0],pos[1],ORANGE)
                    elif rnd == 2:
                        self.host.setColour(pos[0],pos[1],RED)
                self.animatetime = time.monotonic_ns()
        elif self.gamestage == 4:
            # Animate ships to show remaining
            timenow = time.monotonic_ns()
            if timenow - self.turnStarted > TURNTIME * 2:
                self.startGame()
            elif timenow - self.animatetime > ANIMATEINTERVAL:
                print("Game over animation")
                self.flipflop = not self.flipflop
                if self.flipflop:
                    self.drawShip(self.carrier, DIMWHITE, YELLOW)
                    self.drawShip(self.battleship, DIMWHITE, CYAN)
                    self.drawShip(self.cruiser, DIMWHITE, GREEN)
                    self.drawShip(self.submarine, DIMWHITE, MAGENTA)
                    self.drawShip(self.destroyer, DIMWHITE, ORANGE)
                else:
                    self.showShips()
                self.animatetime = time.monotonic_ns()


    def endTurn(self):
        self.activeBtn = (-1,-1)
        self.gamestage = 0
        self.enableBtns = True


    def endGame(self):
        self.gamestage = 4
        # Reset timers for animation of game ended
        self.turnStarted = time.monotonic_ns()
        self.animatetime = self.turnStarted - ANIMATEINTERVAL # Set to time out immediately


    def updateScore(self,colour=YELLOW):
        if self.misses < 12:
            self.host.setColour(self.misses-1, 0, colour)
        elif self.misses < 23:
            self.host.setColour(11, self.misses-12, colour)
        elif self.misses < 34:
            self.host.setColour(34-self.misses, 11, colour)
        elif self.misses < 45:
            self.host.setColour(0, 45-self.misses, colour)


    def checkPositionAgainstShip(self,ship,x,y):
        hit = False
        for i in range(len(ship)):
            pos = ship[i]
            chkX = pos[0]
            chkY = pos[1]
            if chkX == x and chkY == y:
                hit = True
                break
            
        return hit
                

    def checkPositionFree(self,x,y):
        # Check all ships positions
        # Carrier
        hit = self.checkPositionAgainstShip(self.carrier,x,y)
        if hit == False:
            hit = self.checkPositionAgainstShip(self.battleship,x,y)
        if hit == False:
            hit = self.checkPositionAgainstShip(self.cruiser,x,y)
        if hit == False:
            hit = self.checkPositionAgainstShip(self.submarine,x,y)
        if hit == False:
            hit = self.checkPositionAgainstShip(self.destroyer,x,y)
            
        return not hit


    def hitShip(self,ship,x,y):
        intactSections = len(ship)
        result = 0 # Default to miss
        for i in range(len(ship)):
            if x == ship[i][0] and y == ship[i][1]:
                # Mark ship hit
                ship[i][2] = 1
                intactSections += -1
                result = 1
            elif ship[i][2] != 0:
                intactSections += -1

        if result == 1 and intactSections == 0:
            result = 2 # Ship sunk
        
        return result


    def takeShot(self,x,y):
        # Check all ships positions against shot taken at x,y
        # Carrier
        hit = self.hitShip(self.carrier,x,y)
        if hit == 0:
            hit = self.hitShip(self.battleship,x,y)
            if hit == 0:
                hit = self.hitShip(self.cruiser,x,y)
                if hit == 0:
                    hit = self.hitShip(self.submarine,x,y)
                    if hit == 0:
                        hit = self.hitShip(self.destroyer,x,y)
                        if hit == 2:
                            # Sunk ship
                            self.activeShip = self.destroyer
                    elif hit == 2:
                        # Sunk ship
                        self.activeShip = self.submarine
                elif hit == 2:
                    # Sunk ship
                    self.activeShip = self.cruiser
            elif hit == 2:
                # Sunk ship
                self.activeShip = self.battleship
        elif hit == 2:
            # Sunk ship
            self.activeShip = self.carrier

        return hit


    def drawShip(self,ship,colour,hitColour):
        for i in range(len(ship)):
            x = ship[i][0]
            y = ship[i][1]
            if ship[i][2] == 0:
                colour = colour
            else:
                colour = hitColour
            print(f"Drawing in {colour} at {x},{y}")
            self.host.setColour( x, y, colour )
                

    def showShips(self):
        self.drawShip(self.carrier, YELLOW, RED)
        self.drawShip(self.battleship, CYAN, RED)
        self.drawShip(self.cruiser, GREEN, RED)
        self.drawShip(self.submarine, MAGENTA, RED)
        self.drawShip(self.destroyer, ORANGE, RED)
                

    def placeShip(self, ship):
        print(f"Placing ship of size {len(ship)}")
        # Find clear position for ship
        placed = False
        idx = 0
        posX = 0
        posY = 0
        direction = -1
        while placed == False:
            if idx == 0:
                # Place first piece of ship
                # First clear ship position so it does not block itself
                for i in range(len(ship)):
                    ship[i][0] = posX
                    ship[i][1] = posY
                    ship[i][2] = 0
                
                # Pick Random position
                posX = random.randrange(1,11)
                posY = random.randrange(1,11)
                if self.checkPositionFree(posX,posY):
                    ship[idx][0] = posX
                    ship[idx][1] = posY
                    ship[idx][2] = 0
                    idx += 1
                    print(f"Placed first piece at: {posX}, {posY}")
            elif idx < len(ship):
                abort = False
                # Set direction to try and place ship
                if direction < 0:
                    direction = random.randrange(0,3)
                print(f"Direction: {direction}, idx: {idx}")
                # Set position for next part of ship
                if direction == 0:
                    posY += -1
                elif direction == 1:
                    posX += 1
                elif direction == 2:
                    posY += 1
                else:
                    posX += -1
                # Check ship position is still within play area
                if posX > 0 and posX < 11 and posY > 0 and posY < 11:
                    if self.checkPositionFree(posX,posY):
                        ship[idx][0] = posX
                        ship[idx][1] = posY
                        ship[idx][2] = 0
                        print(f"Placed piece {idx} at: {posX}, {posY}")
                        idx += 1
                    else:
                        abort = True
                        print(f"Position {posX},{posY} is not free")
                else:
                    abort = True
                    print(f"Position {posX},{posY} is outside play area")
              
                if abort:
                    # Reset tracking variables to restart placing of ship
                    idx = 0
                    direction = -1
            else:
                placed = True
                print("Ship placed")
        