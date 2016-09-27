# PyHEMTracker
PsychoPy- and PyGaze-based tool for mouse- and eye-tracking decision making experiments with random dots stimulus

Dependencies:

-NumPy

-PsychoPy (https://github.com/psychopy/psychopy/)

-PyGaze (https://github.com/esdalmaijer/PyGaze)

If you want to specify some parameters of psychopy's ElementArrayStim in degrees of visual angle instead of pixels, 
you have to create a monitor profile in the PsychoPy settings. You can do this in two ways:

1) Set the parameters of your monitor in constants.py and run monitor_setup.py

2) Set up the monitor using psychopy's Monitor Center
