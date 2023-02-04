# NeoTrellis hardware code library and virtual simulator
Games and applications to run on virtual and real neotrellis RGB button array hardware.

The real hardware framework program is the Circuit Python file code.py
The virtual (digital twin) simulation of the hardware framework program is the Python file neotrellis-sim.py
The simulator allows development and testing of games and applications written for the neotrellis hardware to be done on a PC, laptop or Raspberry Pi with a screen.

Other files in the src folder of this repo are game or application classes which can run both on the real hardware under Circuit Python (developed on v8.0) and the simulator using pygame on Python 3.7 or later. The game classes which use audio require some overrides of default Python behaviour to allow the code written for the CircuitPython audiocore libraries to run under the pygame engine. To run these game classes under Circuit Python on the real hardware, delete the audio configuration block at the top of the python file (between the comment lines) and uncomment the import line for audiocore. The rest of the class code should work unchanged on real hardware once these changes have been made.
