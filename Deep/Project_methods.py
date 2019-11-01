import os

class Project:
    def __init__(self):
        # TODO: Need to populate these
        # self.processedList = None
        # self.notRatedList = None
        # self.interpolateList = None
        # self.dataFolder = None
        # self.params = None
        # self.mask = ext
        # self.nSubject = None
        # self.nBlock = None
        # self.resultFolder = None
        # self.nProcessedFiles = None
        # self.CGV = None

    def getRatedCount(self):
        return len(self.processedList) - (len(self.notRatedList) + len(self.interpolateList))

    def toBeInterpolatedCount(self):
        return len(self.interpolateList)

    def areFoldersChanged(self):
        # TODO: Implement isFolderChanged
        dataChanged = self.isFolderChanged(self.dataFolder,
        self.nSubject, self.nBlock, self.mask, self.params.Settings.trackAllSteps)
        resultChanged = self.isFolderChanged(self.resultFolder,
        [], self.nProcessedFiles, self.CGV.EXTENSIONS(1).mat, self.params.Settings.trackAllSteps)
        return dataChanged or resultChanged

    @staticmethod
    def makeRatingManually(block, qRate):
        """
        Parameters
        ----------
        block - block for which the rate is returned
        qRate - the rate to be returned

        Returns
        -------
        rate - Return qRate if the block is not rated manually. If
        it is rated manually return 'Manually Rated'.
        """
        rate = None
        if block.isManuallyRated:
            rate = 'Manually Rated'
        else:
            rate = qRate
        return rate
    @staticmethod
    def listSubjects(rootFolder):
        """
        Parameters
        ----------
        rootFolder - the folder in which subjects are looked for

        Returns
        -------
        subjects - list of subjects (dirs) in the folder
        """
        subs = os.path.join(rootFolder)
        subjects = [y for y in os.listdir(subs) if os.path.isdir(y)]

        return subjects
    @staticmethod
    def dirNotHiddens(folder):
        """
        Parameters
        ----------
        folder - The files in this folder are listed

        Returns
        -------
        files - the list of files in the folder, excluding the hidden files
        """

        subs = os.path.join(folder)
        subjects = [y for y in os.listdir(subs) if os.path.isfile(y)]

        return subjects


