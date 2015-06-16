__author__ = 'dankle'

import pytest
import localq.Job

def test_job():
    job = localq.Job(["ls", "-la"], num_cores=1)
    job.set_jobid(1)
    assert job.num_cores == 1
    assert job.cmd == ["ls", "-la"]
    assert job.jobid == 1
    assert job.status() == localq.Job.PENDING
    assert job.priority_method == "fifo"
    assert job.priority() == -1
    job.kill()
    assert job.status() == localq.Job.CANCELLED

    #def __init__(self, cmd, num_cores=1, stdout=None, stderr=None, priority_method="fifo", rundir=None):