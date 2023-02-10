# Example demo class for an interactive game on the NeoTrellis matrix

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

import time

BLANK = (10,10,10)

class RainDemo:
    def __init__(self, host):
        # Host contains all the RGB LED access and audio play methods of the hardware
        self.host = host

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
                        self.host.setColour(drop[0],drop[1]-y,(0,(6-y)*42,0))
                    # Check if above bottom row
                    if drop[1] < 11:
                        # Move down one position
                        drop[1] = drop[1] + 1
                        # Grow drop if not max length already
                        if drop[2] < 6:
                            drop[2] = drop[2] + 1
                        else:
                            # Clear position above drop once full length reached
                            self.host.setColour(drop[0],drop[1]-drop[2]-1,BLANK)
                    else:
                        # Drop has reached bottom row
                        if drop[2] > 0:
                            # Shrink length of tail
                            drop[2] = drop[2] - 1
                            # Clear position above drop as tail shrinks
                            self.host.setColour(drop[0],drop[1]-drop[2]-1,BLANK)
                    
            # Destroy expired drops
            i = len(self.drops)
            while i > 0:
                if self.drops[i-1][2] == 0:
                    deaddrop = self.drops.pop(i-1)
                    self.host.setColour(deaddrop[0],deaddrop[1],BLANK)
                    print(f"Destroyed drop {i-1}")
                i = i - 1
