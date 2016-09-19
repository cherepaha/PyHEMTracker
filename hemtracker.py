from pygaze import libtime
from constants import *
import random
import numpy as np
from hemtracker_ui import HEMTrackerUI
from hemtracker_da import HEMTrackerDA
from hemtracker_et import HEMTrackerET

class HEMTracker:
    rdk_directions = [0., 180.]
    rdk_coherence_values = [0.0, 0.032, 0.064, 0.128, 0.256, 0.512]
    rdk_duration = 800 #msec
                                                               
    exp_info = {}
    
    def __init__(self, user_interface, data_access, eye_tracker):
        self.user_interface = user_interface
        self.data_access = data_access
        self.eye_tracker = eye_tracker
        
        self.exp_info = self.data_access.exp_info
           
    def run_exp(self):
        libtime.expstart()
        self.user_interface.show_intro_screen()
        
        for block_no in range(1, PRACTBLOCKNR+1):
            self.run_block(SESSION_NO, block_no, PRACTBLOCKSIZE, is_practice = True)
        
        for block_no in range(PRACTBLOCKNR+1, PRACTBLOCKNR+RECBLOCKNR+1):
            self.run_block(SESSION_NO, block_no, RECBLOCKSIZE, is_practice = False)
        
        self.eye_tracker.close()
        self.user_interface.close()
        
    def run_block(self, session_number, block_number, block_size, is_practice = False):
        print('start block %i' % block_number)
        self.eye_tracker.calibrate()
        self.user_interface.show_block_intro_screen(block_size, is_practice)
        
        # to make sure that there's equal number of trials for each coherence value,
        # instead of randomly selecting coherence at each trial, we prepare coherence values 
        # for the whole block and then randomly shuffle the list 

        if (block_size % len(self.rdk_coherence_values) != 0):
            raise ValueError('Block size is not divisible by number of conditions!')        
            
        random_coherence_values = np.repeat(np.array(self.rdk_coherence_values), 
                                     block_size/len(self.rdk_coherence_values), axis=0)
        random.shuffle(random_coherence_values)
        
        for trial_no in range(1, block_size+1):
            stim_viewing_log, response_dynamics_log, choice_info = \
                            self.run_trial(session_number, block_number, trial_no, is_practice,
                                           coherence = random_coherence_values[trial_no-1],
                                            direction = random.choice(self.rdk_directions),
                                            duration = self.rdk_duration)
            self.data_access.write_trial_log(stim_viewing_log, response_dynamics_log, choice_info)
            
    def run_trial(self, session_number, block_number, trial_number, is_practice = False, 
                  coherence=0.512, direction = 0.0, duration = 800):
        trial_info = {'subj_id': self.exp_info['subj_id'],
                      'session_no': session_number, 
                      'block_no': block_number,
                      'trial_no': trial_number,
                      'is_practice': is_practice,
                      'coherence': coherence,
                      'direction': direction,
                      'duration': duration}
                      
        self.user_interface.show_ready_screen()
        self.user_interface.show_fixation_screen(random.uniform(FIXATION_DURATION_RANGE[0], 
                                                                FIXATION_DURATION_RANGE[1]))
                        
        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_number, trial_number))

        stim_viewing_log = []
        self.user_interface.show_rdk_EAS(trial_info = trial_info,
                                     tracker = self.eye_tracker,                                     
                                     stim_viewing_log = stim_viewing_log)
        
        response_dynamics_log = []         
        choice_info, response = self.user_interface.show_response_screen(
                                    trial_info = trial_info,                                    
                                    tracker = self.eye_tracker,                                    
                                    response_dynamics_log = response_dynamics_log)
        
        self.eye_tracker.stop_recording()

        self.user_interface.show_feedback_screen(response, trial_info) 

        # drift correction after every fifth trial
        if ((not DUMMYMODE) and (trial_number % 5 == 0)):
            self.eye_tracker.correct_drift()
        
        self.user_interface.show_fixation_screen(300)
        
        return stim_viewing_log, response_dynamics_log, choice_info

hemtracker_ui = HEMTrackerUI()        
hemtracker_da = HEMTrackerDA()
hemtracker_et = HEMTrackerET(user_interface = hemtracker_ui)
hemtracker = HEMTracker(hemtracker_ui, hemtracker_da, hemtracker_et)
hemtracker.run_exp()