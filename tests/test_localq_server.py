__author__ = 'dankle'

import pytest
import localq

def test_server():
    server = localq.LocalQServer(1, 60, "fifo")

    job = localq.Job(["ls", "-la"], num_cores=1)
    server.add(job, 1)

    job2 = localq.Job(["ls", "-lah"], num_cores=1)
    server.add(job2, 2)

    assert len(server.jobs) == 2
    assert server.jobs[0].jobid == 1
    assert server.get_status(1) == localq.Job.PENDING
    server.stop_job_with_id(1)
    assert server.get_status(1) == localq.Job.CANCELLED
    server.stop_all_jobs()
    assert server.get_status(2) == localq.Job.CANCELLED



    #num_cores_available, interval, priority_method