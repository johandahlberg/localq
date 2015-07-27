__author__ = 'dankle'
import subprocess
import os
import datetime
from localq.Status import Status

class Job:

    """ A command line job to run with a specified number of cores
    """
    def __init__(self, cmd, num_cores=1, stdout=None, stderr=None, priority_method="fifo", rundir=None, name=None):
        self.cmd = cmd
        self.num_cores = int(num_cores)
        self.stdout = stdout
        self.stderr = stderr
        self.priority_method = priority_method
        self.rundir = rundir
        self.proc = None
        self.jobid = -1
        self._failed_to_start = False
        self.start_time = None
        self.end_time = None
        self._status = Status.PENDING
        if name is not None:
            self.name = name
        else:
            self.name = None

    def set_jobid(self, jobid):
        self.jobid = jobid
        if self.name is None:
            self.name = "localq-" + str(self.jobid)

    def run(self):
        now = self._get_formatted_now()
        if not self.stdout:
            self.stdout = self.rundir + "/localq-" + str(self.jobid) + "-" + now + ".out"
        if not self.stderr:
            self.stderr = self.rundir + "/localq-" + str(self.jobid) + "-" + now + ".out"
        try:
            self.start_time = now
            self.proc = subprocess.Popen(self.cmd,
                                         stdout=open(self.stdout, 'a'),
                                         stderr=open(self.stderr, 'a'),
                                         cwd=self.rundir)
        except OSError:
            # An OSError is thrown if the executable file in 'cmd' is not found. This needs to be captured
            # "manually" and handled in self.status()
            # see https://docs.python.org/2/library/subprocess.html#exceptions
            self.proc = None
            self._failed_to_start = True

    def _get_formatted_now(self):
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%dT%H%M%S')

    def kill(self):
        """Send the jobs process SIGKILL
        """
        if self.proc:
            try:
                self.proc.kill()
            except OSError:  # if job is finished or has been cancelled before, an OSError will be thrown
                pass
        self._status = Status.CANCELLED

    def update_status(self):
        """
        update the jobs status. Returns nothing.
        :return:
        """
        if self._status == Status.CANCELLED:
            pass
        elif self.proc:
            # update the process' returncode
            self.proc.poll()

            if self.proc.returncode is None:  # Running
                self._status = Status.RUNNING

            else:  # None < 0 evaluates as True on some systems, so need to make sure its not None
                if self.proc.returncode == 0:  # Completed successfully
                    if not self.end_time:
                        self.end_time = self._get_formatted_now()
                    self._status = Status.COMPLETED

                elif self.proc.returncode > 0:  # Failed
                    if not self.end_time:
                        self.end_time = self._get_formatted_now()
                    self._status = Status.FAILED

                elif self.proc.returncode < 0:  # Cancelled
                    if not self.end_time:
                        self.end_time = self._get_formatted_now()
                    # if job was cancelled, returncode will be -N if it received signal N (SIGKILL = 9)
                    self._status = Status.CANCELLED
        else:
            if self._failed_to_start: # Failed to start (self.proc will equal None if this happens)
                if not self.end_time:
                    self.end_time = self._get_formatted_now()
                self._status = Status.FAILED

            else:
                self._status = Status.PENDING

    def status(self):
        """
        Update and return the job's status
        :return: One of Job.PENDING, CANCELLED, COMPLETED, FAILED or RUNNING
        """
        self.update_status()
        return self._status

    def priority(self):
        if self.priority_method == "fifo":
            return -1 * self.jobid
        else:
            ## default to fifo
            return -1 * self.jobid

    def info(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
            str(self.jobid),
            str(self.priority()),
            str(self.status()),
            str(self.num_cores),
            str(self.start_time),
            str(self.end_time),
            str(self.name),
            str(" ".join(self.cmd))
        )
