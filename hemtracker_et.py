from pygaze import eyetracker
from constants import *

# TODO: instead of calling pygaze.calibrate, use pylink.getEYELINK().doTrackerSetup()
# look also at pylink.getEYELINK().enableAutoCalibration()

class HEMTrackerET:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.tracker = eyetracker.EyeTracker(self.user_interface.disp)
    
    def calibrate(self):
        self.tracker.calibrate()
    
    def sample(self):
        return self.tracker.sample()
    
    def pupil_size(self):
        return self.tracker.pupil_size()
    
    def close(self):
        self.tracker.close()
                   
    def start_recording(self, start_message):                        
        self.tracker.start_recording()
        self.tracker.status_msg(start_message)
        self.tracker.log(start_message)
        
    def stop_recording(self):
        self.tracker.stop_recording()
        
    def correct_drift(self):
        checked = False
        while not checked:
            self.user_interface.show_fixation_screen(time = 0)
            checked = self.tracker.drift_correction(fix_triggered=True)