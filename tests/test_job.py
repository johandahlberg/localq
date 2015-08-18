__author__ = 'dankle'

import unittest
import localq.Job
from localq.Status import Status

class TestJob(unittest.TestCase):

    def test_job(self):
        job = localq.Job(["ls", "-la"], num_cores=1, name="testjob")
        job.set_jobid(1)
        assert job.num_cores == 1
        assert job.cmd == ["ls", "-la"]
        assert job.jobid == 1
        assert job.status() == Status.PENDING
        assert job.priority_method == "fifo"
        assert job.priority() == -1
        assert job.name == "testjob"
        job.kill()
        assert job.status() == Status.CANCELLED

        job_with_shell_true = localq.Job("ls -la > /dev/null", num_cores=1, name="testjob_with_shell_true", use_shell=True)
        job_with_shell_true.set_jobid(1)
        assert job_with_shell_true.num_cores == 1
        assert job_with_shell_true.cmd == "ls -la > /dev/null"
        assert job_with_shell_true.jobid == 1
        assert job_with_shell_true.status() == Status.PENDING
        assert job_with_shell_true.priority_method == "fifo"
        assert job_with_shell_true.priority() == -1
        assert job_with_shell_true.name == "testjob_with_shell_true"
        job_with_shell_true.kill()
        assert job_with_shell_true.status() == Status.CANCELLED


        #def __init__(self, cmd, num_cores=1, stdout=None, stderr=None, priority_method="fifo", rundir=None):