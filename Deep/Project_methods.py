import os
import numpy as np


class Project:
    def __init__(self):
        # TODO: remove this before merging with Project.py
        self.processedList = None
        self.notRatedList = None
        self.interpolateList = None
        self.dataFolder = None
        self.params = None
        self.mask = ext
        self.nSubject = None
        self.nBlock = None
        self.resultFolder = None
        self.nProcessedFiles = None
        self.CGV = None

    def get_current_block(self):
        """
        Return the block pointed by the current index.If current is -1, a mock block is returned.
        Returns
        -------
        block : object
            Current block

        """
        if self.current == -1:
            subject = Subject('','')
            block = Block(self, subject, '', '', self.CGV)
            block.index = -1
            return

        unique_name = self.processed_list(self.current)
        block = self.block_map(unique_name)
        return block

    def update_rating_lists(self, block):
        """

        Parameters
        ----------
        block

        Returns
        -------

        """
        if block.rate == self.CGV.RATINGS.Good:
            if not np.isin(block.index, self.good_list):
                self.good_list.append(block.index)
                self.not_rated_list[self.not_rated_list == block.index] = ""
                self.ok_list[self.ok_list == block.index] = ""
                self.bad_list[self.bad_list == block.index] = ""
                self.interpolate_list[self.interpolate_list == block.index] = ""
                self.good_list = np.unique(self.good_list)

        elif block.rate == self.CGV.RATINGS.OK:
            if not np.isin(block.index, self.ok_list):
                self.ok_list.append(block.index)
                self.not_rated_list[self.not_rated_list == block.index] = ""
                self.good_list[self.good_list == block.index] = ""
                self.bad_list[self.bad_list == block.index] = ""
                self.interpolate_list[self.interpolate_list == block.index] = ""
                self.ok_list = np.unique(self.ok_list)

        elif block.rate == self.CGV.RATINGS.Bad:
            if not np.isin(block.index, self.bad_list):
                self.bad_list.append(block.index)
                self.not_rated_list[self.not_rated_list == block.index] = ""
                self.good_list[self.good_list == block.index] = ""
                self.ok_list[self.ok_list == block.index] = ""
                self.interpolate_list[self.interpolate_list == block.index] = ""
                self.bad_list = np.unique(self.bad_list)

        elif block.rate == self.CGV.RATINGS.Interpolate:
            if not np.isin(block.index, self.interpolate_list):
                self.interpolate_list.append(block.index)
                self.not_rated_list[self.not_rated_list == block.index] = ""
                self.good_list[self.good_list == block.index] = ""
                self.ok_list[self.ok_list == block.index] = ""
                self.bad_list[self.bad_list == block.index] = ""
                self.interpolate_list = np.unique(self.interpolate_list)

        elif block.rate == self.CGV.RATINGS.NotRated:
            if not np.isin(block.index, self.not_rated_list):
                self.not_rated_list.append(block.index)
                self.bad_list[self.bad_list == block.index] = ""
                self.good_list[self.good_list == block.index] = ""
                self.ok_list[self.ok_list == block.index] = ""
                self.interpolate_list[self.interpolate_list == block.index] = ""
                self.not_rated_list = np.unique(self.not_rated_list)

                return self

    def update_rating_structures(self):
        """
        Updates the data structures of this project. Look
        createRatingStructure() for more info.
        This method may be time consuming depending on the number of
        files in both dataFolder and resultFolder as it goes
        through every block and fetches relevant information.

        This functionality helps to merge different projects
        together. As it goes through all files in the dataFolder and
        resultFolder, it finds out the new files that are added to
        these folders, and updates the data correspondigly. If
        there are raw files added to the dataFolder only, it means some
        new subjects are added. If there are raw files added to the
        dataFolder and they have also their corresponding new
        preprocessed files in the resultFolder, it means that some
        data from another projects are added to this project. If
        there are some new preprocessed files added to the
        resultFolder only , they will be considered only if a
        corresponding rawData in the dataFolder exist. Otherwise they
        are ignored.
        If on the other hand, any files is deleted from any of those
        two folders, they are not copied to the new data structures
        and considered as deleted files in the project.
        Returns
        -------

        """

    def get_rated_count(self):
        """

        Returns
        -------

        """
        return len(self.processed_list) - (len(self.not_rated_list) + len(self.interpolate_list))

    def to_be_interpolated_count(self):
        return len(self.interpolate_list)

    def are_folders_changed(self):
        # TODO: Implement isFolderChanged
        data_changed = self.isFolderChanged(self.dataFolder,
        self.nSubject, self.nBlock, self.mask, self.params.Settings.trackAllSteps)
        result_changed = self.isFolderChanged(self.resultFolder,
        [], self.nProcessedFiles, self.CGV.EXTENSIONS(1).mat, self.params.Settings.trackAllSteps)
        return data_changed or result_changed

    @staticmethod
    def make_rating_manually(block, q_rate):
        """
        Parameters
        ----------
        block - obj
            block for which the rate is returned
        qRate - str
            the rate to be returned

        Returns
        -------
        rate - Return qRate if the block is not rated manually. If
        it is rated manually return 'Manually Rated'.
        """
        rate = None
        if block.isManuallyRated:
            rate = 'Manually Rated'
        else:
            rate = q_rate
        return rate

    @staticmethod
    def list_subjects(root_folder):
        """
        Parameters
        ----------
        rootFolder - the folder in which subjects are looked for

        Returns
        -------
        subjects - list of subjects (dirs) in the folder
        """
        subs = os.path.join(root_folder)
        subjects = [y for y in os.listdir(subs) if os.path.isdir(y)]

        return subjects

    @staticmethod
    def dir_not_hiddens(folder):
        """
        Parameters
        ----------
        folder - The files in this folder are listed

        Returns
        -------
        files - the list of files in the folder, excluding the hidden files
        """

        subs = os.path.join(folder)
        files = [y for y in os.listdir(subs) if os.path.isfile(y)]

        return files
