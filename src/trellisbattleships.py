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

TURNTIME = 1000000000
ANIMATEINTERVAL = 500000000

"""
No. Class of ship Size
1   Carrier        5
2   Battleship     4
3   Cruiser        3
4   Submarine      3
5   Destroyer      2
"""

class Battleships:
    def __init__(self, getColour, setColour):
        self.getColour = getColour
        self.setColour = setColour

        self.carrier = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.battleship = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.cruiser = [[0,0,0],[0,0,0],[0,0,0]]
        self.submarine = [[0,0,0],[0,0,0],[0,0,0]]
        self.destroyer = [[0,0,0],[0,0,0]]

        self.enableBtns = False
        self.btnDown = False
        self.activeBtn = (-1,-1)
        self.turnStarted = 0 #0 indication no turn active, otherwise the time the turn started is stored
        self.gamestage = 0 # 0=waiting for player to take shot; 1=shot fired; 2=ship hit; 3=ship sinking
        
        self.startGame()
        self.enableBtns = True


    def startGame(self):
        self.enableBtns = False
        # Draw border
        for x in range(12):
            self.setColour( x, 0, GREEN )
            self.setColour( x, 11, GREEN )
        for y in range(12):
            self.setColour( 0, y, GREEN )
            self.setColour( 11, y, GREEN )
        # Draw playing area
        for y in range(1,11):
            for x in range(1,11):
                self.setColour( x, y, NOTTRIED )
        # Place ships
        self.placeShip(self.carrier)
        self.placeShip(self.battleship)
        self.placeShip(self.cruiser)
        self.placeShip(self.submarine)
        self.placeShip(self.destroyer)

        # Reset Score Tracking
        self.misses = 0
        self.remainingships = 5

        #self.showShips()


    def btnEvent(self, x, y, press):
        if self.enableBtns:
            if press:
                # Only allow one button to be down at a time
                if self.btnDown == False:
                    # Check if a valid button selection for the game
                    if 0 < x < 11 and 0 < y < 11 and self.getColour(x,y) == NOTTRIED:
                        self.btnDown = True
                        self.activeBtn = (x,y)
                        self.setColour(x,y,WHITE,False)
            else:
                # Only act on release of the active button
                if x == self.activeBtn[0] and y == self.activeBtn[1]:
                    self.enableBtns = False
                    self.btnDown = False
                    self.turnStarted = time.monotonic_ns()
                    self.animatetime = self.turnStarted - ANIMATEINTERVAL # Set to time out immediately
                    self.gamestage = 1
                    

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
                    self.setColour(self.activeBtn[0],self.activeBtn[1],BLUE)
                    self.endTurn()
                else:
                    self.gamestage = outcome + 1
            elif timenow - self.animatetime > ANIMATEINTERVAL:
                print("turn animating")
                self.animatetime = time.monotonic_ns()
                # Flash button
                if self.getColour(self.activeBtn[0],self.activeBtn[1]) != YELLOW:
                    self.setColour(self.activeBtn[0],self.activeBtn[1],YELLOW)
                else:
                    self.setColour(self.activeBtn[0],self.activeBtn[1],NOTTRIED)
        elif self.gamestage == 2:
            # Ship hit
            self.setColour(self.activeBtn[0],self.activeBtn[1],ORANGE)
            self.endTurn()
        elif self.gamestage == 3:
            # Ship sunk
            self.setColour(self.activeBtn[0],self.activeBtn[1],RED)
            self.endTurn()


    def endTurn(self):
        self.activeBtn = (-1,-1)
        self.gamestage = 0
        self.enableBtns = True


    def updateScore(self):
        if self.misses < 12:
            self.setColour(self.misses-1, 0, YELLOW)
        elif self.misses < 23:
            self.setColour(11, self.misses-12, YELLOW)
        elif self.misses < 34:
            self.setColour(34-self.misses, 11, YELLOW)
        elif self.misses < 45:
            self.setColour(0, 45-self.misses, YELLOW)


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
            self.setColour( x, y, colour )
                

    def showShips(self):
        self.drawShip(self.carrier, YELLOW, RED)
        self.drawShip(self.battleship, CYAN, RED)
        self.drawShip(self.cruiser, PURPLE, RED)
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
        