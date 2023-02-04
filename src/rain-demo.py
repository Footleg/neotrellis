import time

class RainDemo:
    def __init__(self, getColour, setColour):
        self.getColour = getColour
        self.setColour = setColour
        self.drops = []
        self.tick = time.monotonic_ns()

    def btnEvent(self, x, y, press):
        if press:
            # Start rain drop at this position
            self.drops.append([x,y,1])

    def animate(self):
        # Increment animations which run independent of button presses (if any)
        if time.monotonic_ns() - self.tick > 200000000:
            self.tick = time.monotonic_ns()
            # Update raindrops
            for drop in self.drops:
                if drop[2] > 0:
                    # Render drop
                    for y in range(drop[2]):
                        # Draw length, brightest at bottom, fading to top
                        self.setColour(drop[0],drop[1]-y,(0,(6-y)*42,0))
                    # Check if above bottom row
                    if drop[1] < 11:
                        # Move down one position
                        drop[1] = drop[1] + 1
                        # Grow drop if not max length already
                        if drop[2] < 6:
                            drop[2] = drop[2] + 1
                        else:
                            # Clear position above drop once full length reached
                            self.setColour(drop[0],drop[1]-drop[2]-1,(10,10,10))
                    else:
                        # Drop has reached bottom row
                        if drop[2] > 0:
                            # Shrink length of tail
                            drop[2] = drop[2] - 1
                            # Clear position above drop as tail shrinks
                            self.setColour(drop[0],drop[1]-drop[2]-1,(10,10,10))
                elif drop[1] == 11:
                    # Clean up empty drop
                    self.setColour(drop[0],drop[1],(10,10,10))
                    # Move to top row to indicate it can be cleaned from array
                    drop[1] = 0
                    
            # Destroy expired drops
            """
            i = len(self.drops)
            while i > 0:
                if self.drops[i-1][1] == 0:
                    self.drops.remove[i-1]
                    print(f"Destroyed drop {i-1}")
                i = i - 1
            """                
