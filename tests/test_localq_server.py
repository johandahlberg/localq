__author__ = 'dankle'

import pytest
import localq

def test_server():
    #LocalQServer(num_cores, interval, priority_type)
    server = localq.LocalQServer(1, 60, "fifo")

    # add(cmd, num_cores)
    server.add(["ls", "-la"], 1)
    server.add(["ls", "-lah"], 2)

    assert len(server.jobs) == 1  # since job2 requests 2 cores, but only 1 is available

    server.add(["ls", "-lah"], 1)

    assert len(server.jobs) == 2  # since job2 requests 2 cores, but only 1 is available

    assert server.jobs[0].jobid == 1
    assert server.get_status(1) == localq.Job.PENDING
    server.stop_job_with_id(1)
    assert server.get_status(1) == localq.Job.CANCELLED
    server.stop_all_jobs()
    assert server.get_status(2) == localq.Job.CANCELLED



    #num_cores_available, interval, priority_method