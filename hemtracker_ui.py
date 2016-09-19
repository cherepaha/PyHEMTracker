from __future__ import division
from psychopy import visual
from pygaze import libscreen, libtime, libinput
import pygaze
from constants import *
import numpy as np

class HEMTrackerUI:
    ready_button_width = 100
    ready_button_height = 40
    arrow_pos_left = (150,150)    
    arrow_pos_right = (DISPSIZE[0]-150, 150)    
    arrow_diameter = 250
    
    rdk_dir = 0.0
    rdk_coherence = 0.0
    rdk_duration = 0
    
    # this has to correspond to the parameters set for show_rdk_EAS()
    n_dots = 3

    def __init__(self):
        self.disp = libscreen.Display(monitor = MONITOR_LABEL)
        self.mouse = libinput.Mouse(visible=True)
        self.keyboard = libinput.Keyboard(keylist=['space', 'left', 'right', 'lctrl', 'rctrl'], 
                                          timeout=None)

        self.blank_screen = libscreen.Screen()

        self.intro_screen = libscreen.Screen()
#        self.intro_screen.set_background_colour(colour='black')
        self.intro_screen.draw_text(text='During each trial, a cloud of moving dots is going to \
                                            appear on the screen. Watch it carefully to detect \
                                            whether the dots in general are moving to the left or \
                                            to the right (click left mouse button to start)', 
                                            fontsize=18)
        
        self.fixation_screen = libscreen.Screen()
        self.fixation_screen.draw_fixation(fixtype='cross', pw=3)
        
        self.ready_screen = libscreen.Screen()
        self.ready_screen.draw_text(text='Click the Start button to start the trial',  fontsize=18)
        self.ready_screen.draw_rect(colour=(200,200,200), x=DISPSIZE[0]/2-self.ready_button_width/2, 
                            y=DISPSIZE[1]-30-self.ready_button_height/2,
                            w=self.ready_button_width, h=self.ready_button_height, pw=3)
        self.ready_screen.draw_text(text='Start', 
                            pos=(DISPSIZE[0]/2, DISPSIZE[1]-30), fontsize=18)                            
        
        self.stimuli_screen = libscreen.Screen()
        self.dot_stim = visual.ElementArrayStim(pygaze.expdisplay, elementTex=None, 
                                                fieldShape='circle', elementMask='circle', 
                                                sizes=0.06, nElements = self.n_dots,
                                                units='deg', fieldSize = 5.0)        
        self.stimuli_screen.screen.append(self.dot_stim)

        self.response_screen = libscreen.Screen()
        self.response_screen.draw_image('images/arrow_left_inv.png', pos=self.arrow_pos_left)
        self.response_screen.draw_image('images/arrow_right_inv.png', pos=self.arrow_pos_right)

        self.left_pos_feedback_screen = libscreen.Screen()                
        self.left_pos_feedback_screen.draw_circle(colour=(52,201,64), pos=self.arrow_pos_left, 
                                                   r=self.arrow_diameter/2, fill=True)
        self.left_neg_feedback_screen = libscreen.Screen()
        self.left_neg_feedback_screen.draw_circle(colour=(196,46,46), pos=self.arrow_pos_left, 
                                                   r=self.arrow_diameter/2, fill=True)
        self.right_pos_feedback_screen = libscreen.Screen()
        self.right_pos_feedback_screen.draw_circle(colour=(52,201,64), pos=self.arrow_pos_right, 
                                                   r=self.arrow_diameter/2, fill=True)
        self.right_neg_feedback_screen = libscreen.Screen()
        self.right_neg_feedback_screen.draw_circle(colour=(196,46,46), pos=self.arrow_pos_right, 
                                                   r=self.arrow_diameter/2, fill=True)
    
    def close(self):
        self.disp.close()
    
    def show_intro_screen(self):
        self.disp.fill(self.intro_screen)
        self.disp.show()
        if KEYBOARD_MODE:
            self.keyboard.get_key()
        else:
            self.mouse.get_clicked()
        libtime.pause(300)
        
    def show_block_intro_screen(self, block_size, is_practice):
        self.mouse.set_visible(True)
        self.block_intro_screen = libscreen.Screen()
        block_type = 'practice' if is_practice else 'recorded'
        self.block_intro_screen.draw_text(text='You are about to start the block of %d %s trials.\
                                    To start click left mouse button.' % (block_size, block_type), 
                                    fontsize=18)
        self.disp.fill(self.block_intro_screen)
        self.disp.show()
        if KEYBOARD_MODE:
            self.keyboard.get_key()
        else:
            self.mouse.get_clicked()
        libtime.pause(300)
        
    def show_ready_screen(self):
        self.mouse.set_visible(True)
        self.disp.fill(self.ready_screen)
        self.disp.show()
        
        if(KEYBOARD_MODE):
            self.keyboard.get_key()
        else:
            while True:
                mouse_position = self.mouse.get_pos()
                if ((self.mouse.get_pressed()[0]==1) and 
                    (abs(mouse_position[0]-DISPSIZE[0]/2)<self.ready_button_width/2) and 
                    (abs(mouse_position[1]-DISPSIZE[1]+30)<self.ready_button_height/2)):
                        break
#        libtime.pause(300)        
                        
    def show_fixation_screen(self, time = 0):
        self.mouse.set_visible(False)
        self.disp.fill(self.fixation_screen)
        self.disp.show()
        libtime.pause(time)
        
    def show_rdk_EAS(self, direction, coherence, tracker, trial_info, stim_viewing_log, 
                     duration = 800, n_sequences = 3, density = 16.7, dot_speed = 5.0, 
                     dot_lifetime = 3, frame_rate = 60, field_size = 5.0, field_scale = 1.1):
                         
        self.mouse.set_visible(False)

        self.rdk_dir = direction
        self.rdk_coherence = coherence
        self.rdk_duration = duration

        field_width = field_size*field_scale
        n_dots = int(np.ceil(density * field_width**2 / frame_rate))
        
        # due to ElementArrayStim limitations, n_dots has to be divisible by n_sequences
        # so we artificially add 
        n_dots += (n_sequences - n_dots % n_sequences) % n_sequences
        # the resulting n_dots should be divided by n_sequences and set as the nDots parameter 
        # of ElementArrayStim in  __init__ (currently 3, given density = 16.7)

        # stores logical index of the dots belonging to current sequence
        current_sequence_dots = np.zeros(n_dots, dtype=bool)
        
        # dot displacement (in visual angle degrees) per n_sequence frames
        displacement = (dot_speed/field_size) * n_sequences / frame_rate
        deltaX = displacement*np.cos(np.pi*direction/180.0)
        deltaY = displacement*np.sin(np.pi*direction/180.0)
            
        dot_positions = np.random.rand(2, n_dots)

        stim_start_time = libtime.get_time()
        t = 0
        current_sequence = -1
        
        while t  < duration:
            t = libtime.get_time() - stim_start_time
            current_sequence = (current_sequence + 1) % n_sequences
            # first, set all values to False
            current_sequence_dots[current_sequence_dots] = False
            # second, set to True the values corresponding to the dots belonging to current sequence
            current_sequence_dots[current_sequence::n_sequences] = True
            
            # number of dots in the current frame, alternatively calculated as n_dots/n_sequences
            current_n_dots = sum(current_sequence_dots)
            
            coherent_dots = np.zeros(len(current_sequence_dots), dtype=bool)
            # for each dot in the current sequence, randomly determine on each frame whether 
            # the dot should be coherently or randomly moved
            # coherent_rand is set to True for those dots of the current frame 
            # which are coherently moved
            coherent_rand = np.random.rand(current_n_dots) < coherence
            n_coherent_dots = sum(coherent_rand)
            n_noncoherent_dots = current_n_dots - n_coherent_dots
            
            # TODO: now assume lifetime is unlimited. Implement limited lifetime
            
            coherent_dots[current_sequence_dots] = coherent_rand
            
            non_coherent_dots = current_sequence_dots.copy()
            non_coherent_dots[coherent_dots] = False
                        
            dot_positions[0, coherent_dots] += deltaX
            dot_positions[1, coherent_dots] += deltaY
            
            # Move non-coherent dots to a random position so they flicker
            # rather than walk randomly (with random velocity)
            dot_positions[:, non_coherent_dots] = np.random.rand(2, n_noncoherent_dots)
            
            # if a dot goes outside the aperture, replace it randomly 
            # rather than move it to the opposite side
            out_dots = np.any((dot_positions < 0) | (dot_positions > 1), axis=0)
            dot_positions[:, out_dots] = np.random.rand(2, sum(out_dots))
            
            self.dot_stim.setXYs(((dot_positions[:,current_sequence_dots]-0.5)*field_size).transpose())
            self.dot_stim.draw()
            
            self.disp.fill(screen=self.stimuli_screen)            
            self.disp.show()
            
            mouse_position = self.mouse.get_pos()
            eye_position = tracker.sample()
            pupil_size = 0 if DUMMYMODE else tracker.pupil_size()
            
            stim_viewing_log.append([trial_info['subj_id'], trial_info['session_no'], 
                                     trial_info['block_no'], 
                                     trial_info['trial_no'], str(t), mouse_position[0], 
                                     mouse_position[1], eye_position[0], 
                                     eye_position[1], pupil_size])
        
    def show_response_screen(self, tracker, trial_info, response_dynamics_log):
        self.mouse.set_visible(True)
        self.mouse.set_pos((DISPSIZE[0]/2, DISPSIZE[1]-30))
        
        self.disp.fill(screen=self.response_screen)
        self.disp.show()
        
        trial_start_time = libtime.get_time()
        
        # keyboard mode
        
        if(KEYBOARD_MODE):
            response_key, trial_end_time = self.keyboard.get_key(timeout=None)
            response = 0 if (response_key=='right') or (response_key=='rctrl') else 180
            response_time  = trial_end_time - trial_start_time
        else:
        # mouse mode 
            while(True):     
                t = libtime.get_time() - trial_start_time
                mouse_position = self.mouse.get_pos()
                eye_position = tracker.sample()
                pupil_size = 0 if DUMMYMODE else tracker.pupil_size()
                
                response_dynamics_log.append([trial_info['subj_id'], trial_info['block_no'], 
                                     trial_info['trial_no'], str(t), mouse_position[0], 
                                    mouse_position[1], eye_position[0], 
                                    eye_position[1], pupil_size])
                libtime.pause(TIMESTEP)
                
                if (self.mouse.get_pressed()[0]==1):
                    if (((mouse_position[0]-self.arrow_pos_left[0])**2 +
                            (mouse_position[1]-self.arrow_pos_left[1])**2 < 
                                self.arrow_diameter**2/4) or 
                        ((mouse_position[0]-self.arrow_pos_right[0])**2 +
                            (mouse_position[1]-self.arrow_pos_right[1])**2 < 
                                self.arrow_diameter**2/4)):
                            break
                # 180: 'left' response
                # 0 'right' response
            response = 0 if self.mouse.get_pos()[0]-DISPSIZE[0]/2>0 else 180
            response_time = libtime.get_time()-trial_start_time

        choice_info = [trial_info['subj_id'], trial_info['session_no'], trial_info['block_no'], 
                       trial_info['trial_no'], trial_info['is_practice'], self.rdk_dir, 
                        self.rdk_coherence, self.rdk_duration, response, response_time]
                      
        return choice_info, response

    def show_feedback_screen(self, response):
        self.mouse.set_visible(False)
        if (response==self.rdk_dir):
            if (response==0):
                self.disp.fill(self.right_pos_feedback_screen)
            else:
                self.disp.fill(self.left_pos_feedback_screen)
        else:
            if (response==0):
                self.disp.fill(self.right_neg_feedback_screen)
            else:
                self.disp.fill(self.left_neg_feedback_screen)

        self.disp.show()
        libtime.pause(300)