from typing import List
import logging
import numpy as np
from pyautomagic.src.calcQuality import calcQuality

logger = logging.getLogger(__name__)

class Block():
    def __init__(self,project,subject,data_name,data_path):
        self.project = project
        self.subject = subject
        self.data_name = data_name
        self.data_path = data_path
        self.unique_name = extract_unique_filename(self)
        self.params = project.params
        self.data_extension = project.data_extension
        self.sampling_rate = project.sampling_rate
        
    def extract_unique_filename(self):
        #return new block name from the info used to initiate the block
        
    def update_rating_from_file(self):
            #check to see if a results file exists where we think it should
            # if it does, check if the parameters match the project current
            # if params don't match, error out cause you have to reprocess
            # check the prefix and if its empty, theres no rating yet
            # if no rating, update the block with the not rated info
            # if a rating exists, pull out the info and update the block
            # update the result file path/name
        self.result_name = potential_result_name(self)
    def potential_result_path(self):
        # based on the data file path and name info, make a result name and path
        return result_name
    def extract_prefix(self,result_path):
        # checks the string of the results, makes sure it matches one of the valid ones
        # returns a code for the prefix
        
    def has_info(self,prefix: str):
        # if its been interpolated or has been rated, it has info
        # just looks at the string and makes the determination
    def extract_rate_from_prefix(self,prefix: str):
        # justcompares strings and says what they mean
        
    def update_addresses(self,new_data_path,new_project_path):
        # used for when loading from a different computer, low priority rn
    def preprocess(self):
        data = load_data(self)
        # do some parameter checks
        # use externally written function to preprocess
        # calcQuality
        # update self.Quality
        # store a bunch of stuff into an automagic object for results file
        # save files
        # write log
    def load_data(self):
        # mostly from eeglab, need to use MNE here
        # must account for all possible data types
    def update_rating(self,update):
        # update can have many fields, go through and see what they are and update the block accordingly

    def save_all_files(self):
        # save the processed stuff and figures into results path
    def write_log(self):
        #
    def interpolate(self):
        # load up the preprocessed results file from results location
        # perform the interpolation (uses some EEGLab stuff I believe)
        # calcQuality
        # update block info, update results file info
        # save fils
        # write log
    def update_prefix(self):
        # updates every time its interpolated and rated
        # must be restricted so you can't just lie and stuff
    def save_ratings(self):
        # get the preprocessed file and do updates from Block info
        # write log
    def update_result_path(self):
        # checks if the naming is good previously
        # updates name based on ratings
    def extract_reduced_address(self):
        # like 2 lines of string stuff, for if we want to save downsampled version