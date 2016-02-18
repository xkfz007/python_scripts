# A simple task manager

import subprocess
import time
from multiprocessing import cpu_count
import log


class TaskManager:
    m_maxTaskNumber = 1
    TaskKeeper = {}  # TaskKeeper is a dictionary
    # m_cmdListsAndLogFiles = [] # A list to store all the command List
    m_LogOut = log.Log('taskmanager')

    def __init__(self, maxTN=1):

        if maxTN > cpu_count():
            self.m_LogOut.error("  %d workers, %d cpu cores\n" % (maxTN, cpu_count()))
            self.m_maxTaskNumber = cpu_count() - 1
        else:
            self.m_LogOut.warning("  %d workers, %d cpu cores\n" % (maxTN, cpu_count()))
            self.m_maxTaskNumber = maxTN
        self.TaskKeeper = {}
        # self.m_cmdListsAndLogFiles = []


    def newTask(self, command, outFileName=None):
        '''
        execute command and dump the log into file
        params:
            command        : the command to execute
            outFileName    : dump the log to this file
        '''
        if len(self.TaskKeeper) < self.m_maxTaskNumber:
            if command != "":
                if outFileName != None:
                    outFile = open(outFileName, 'w')
                    self.m_LogOut.warning("Add new task: " + command + '\n')
                    self.TaskKeeper.update({command: subprocess.Popen(command, stdout=outFile, stderr=outFile)})
                else:
                    self.m_LogOut.warning("Add new task: " + command + '\n')
                    self.TaskKeeper.update({command: subprocess.Popen(command, stdout=None, stderr=None)})

        else:
            # Wait until TaskKeeper has free space
            while True:
                time.sleep(0.1)
                for cmd, tsk in self.TaskKeeper.items():
                    if tsk.poll() != None:  # Means task has terminated
                        self.TaskKeeper.pop(cmd)

                if (len(self.TaskKeeper) < self.m_maxTaskNumber):
                    break

            self.newTask(command, outFileName)


    def clearAllTask(self):
        '''
        Call after all newTask() has been called.
        '''

        while True:
            if (len(self.TaskKeeper) == 0):  # wait until all task finished
                self.m_LogOut.info("All tasks are finished!")
                break
            for command, task in self.TaskKeeper.items():
                if task.poll() != None:
                    self.TaskKeeper.pop(command)
            time.sleep(0.1)


            # def __del__(self):
            #  self.clearAllTask()


