import os
import signal
import subprocess
import datetime
from localq.Status import Status

__author__ = 'dankle'


class Job:

    """ A command line job to run with a specified number of cores
    """
    def __init__(self, job_id, cmd, num_cores=1, stdout=None, stderr=None,
                 rundir=".", name=None, use_shell=False, dependencies=[]):
        self.jobid = job_id
        self.cmd = cmd
        self.num_cores = int(num_cores)
        self.stdout = stdout
        self.stderr = stderr
        self.rundir = rundir
        self.proc = None
        self._failed_to_start = False
        self.start_time = None
        self.end_time = None
        self._status = Status.PENDING
        self.use_shell = use_shell
        self.dependencies = dependencies

        if name is None:
            self.name = "localq-" + str(self.jobid)
        else:
            self.name = name

    def run(self):
        now = self._get_formatted_now()
        if not self.stdout:
            self.stdout = str(self.rundir) + "/localq-" + str(self.jobid) + "-" + now + ".out"
        if not self.stderr:
            self.stderr = str(self.rundir) + "/localq-" + str(self.jobid) + "-" + now + ".out"
        try:
            self.start_time = now
            self.proc = subprocess.Popen(self.cmd,
                                         shell=self.use_shell,
                                         stdout=open(self.stdout, 'a'),
                                         stderr=open(self.stderr, 'a'),
                                         cwd=self.rundir,
                                         preexec_fn=os.setsid
                                         )
        except OSError:
            # An OSError is thrown if the executable file in 'cmd' is not found. This needs to be captured
            # "manually" and handled in self.status()
            # see https://docs.python.org/2/library/subprocess.html#exceptions
            self.proc = None
            self._failed_to_start = True

    @staticmethod
    def _get_formatted_now():
        return datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

    def kill(self):
        """Send the jobs process SIGTERM
        """
        if self.proc:
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
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

    def info(self):
        return "\t".join(
            [str(self.jobid),
             str(self.status()),
             str(self.num_cores),
             str(self.start_time),
             str(self.end_time),
             str(self.name),
             str(" ".join(self.cmd))]
        )

    def __hash__(self):
        return self.jobid

    def __str__(self):
        return str(self.jobid) + "-" + str(self.name)
