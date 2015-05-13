__author__ = 'dankle'
import subprocess

class Job:
    """ A command line job to run with a specified number of cores
    """
    def __init__(self, cmd, num_cores=1):
        self.cmd = cmd
        self.num_cores = num_cores
        self.jobid = -1

    def set_jobid(self, jobid):
        self.jobid = jobid

    def run(self):
        print "Running job {}".format(self.jobid)
        subprocess.Popen(self.cmd)

    def kill(self):
        pass

    def status(self):
        pass