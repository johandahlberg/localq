__author__ = 'dankle'
import subprocess
import os

class Job:

    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"

    """ A command line job to run with a specified number of cores
    """
    def __init__(self, cmd, num_cores=1, stdout="/dev/null", stderr="/dev/null", priority_method="fifo", rundir=None):
        self.cmd = cmd
        self.num_cores = int(num_cores)
        self.stdout = stdout
        self.stderr = stderr
        self.priority_method = priority_method
        self.rundir = rundir
        self.proc = None
        self.jobid = -1

    def set_jobid(self, jobid):
        self.jobid = jobid

    def run(self):
        try:
            if self.rundir:
                os.chdir(self.rundir)
            self.proc = subprocess.Popen(self.cmd, stdout=open(self.stdout, 'a'), stderr=open(self.stderr, 'a'))
        except OSError:
            print "job failed to run, are there pipes in the command line?"

    def kill(self):
        pass

    def status(self):
        if self.proc:
            self.proc.poll()

            if self.proc.returncode is not None and self.proc.returncode == 0:
                return Job.COMPLETED
            elif self.proc.returncode > 0:
                return Job.FAILED + "/" + str(self.proc.returncode)
            if self.proc.returncode is None:
                return Job.RUNNING
        else:
            return Job.PENDING

    def priority(self):
        if self.priority_method == "fifo":
            return -1 * self.jobid
        else:
            return self.jobid

    def info(self):
        return "{}\t{}\t{}\t{}\t{}\t{}".format(
            str(self.jobid),
            str(self.priority()),
            str(self.status()),
            str(self.num_cores),
            str(self.priority_method),
            str(self.cmd)
        )
