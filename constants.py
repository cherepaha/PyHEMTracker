SUBJ_ID = None
SESSION_NO = 1

KEYBOARD_MODE = True
ID_RANGE = [101, 999]

#RDK_DURATION = 800
FIXATION_DURATION_RANGE = [700, 1000]
TIMESTEP = 10 # mouse sampling interval, msec

# Important: number of trials per block should be divisible by number of conditions
PRACTBLOCKNR = 0 # number of practice blocks
PRACTBLOCKSIZE = 50 # number of practice trials per block
RECBLOCKNR = 1 # number of recorded blocks
RECBLOCKSIZE = 6 # number of recorded trials per block

# EYETRACKER
TRACKERTYPE = 'dummy' # either 'smi', 'eyelink' or 'dummy' (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
DUMMYMODE = True # False for gaze contingent display, True for dummy mode (using mouse or joystick)
LOGFILENAME = 'eyedata' # logfilename, without path
LOGFILE = LOGFILENAME[:] # .txt; adding path before logfilename is optional; logs responses (NOT eye movements, these are stored in an EDF file!)
EVENTDETECTION = 'native'

# DISPLAY
MONITOR_LABEL = 'hemtracker_monitor'
MONITOR_DISTANCE = 60 # distance from eyes to monitor in cm
SCREENNR = 0 # number of the screen used for displaying experiment
MONITOR = 'hemtracker_monitor'
DISPTYPE = 'psychopy' # either 'psychopy' or 'pygame'
DISPSIZE = (1366,768) # canvas size
SCREENSIZE = (31., 18.) # physical display size in cm
#BGC = (125,125,125,255) # backgroundcolour
#FGC = (0,0,0,255) # foregroundcolour
BGC = (0,0,0,255) # backgroundcolour
FGC = (255,255,255,255) # foregroundcolour
