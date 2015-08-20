__author__ = 'dankle'

import unittest
import localq
import time
from localq.Status import Status

class TestLocalQServer(unittest.TestCase):


    def test_server(self):
        #LocalQServer(num_cores, interval, priority_type)
        server = localq.LocalQServer(1, 60, "fifo")

        # add(cmd, num_cores)
        server.add(["ls", "-la"], 1)
        server.add(["ls", "-lah"], 2)

        assert len(server.jobs()) == 1  # since job2 requests 2 cores, but only 1 is available

        server.add(["ls", "-lah"], 1)

        assert len(server.jobs()) == 2  # since job2 requests 2 cores, but only 1 is available

        assert server.jobs()[0].jobid == 1
        assert server.get_status(1) == Status.PENDING
        server.stop_job_with_id(1)
        assert server.get_status(1) == Status.CANCELLED
        server.stop_all_jobs()
        assert server.get_status(2) == Status.CANCELLED

        #num_cores_available, interval, priority_method

    def test_get_status_for_all(self):
        server = localq.LocalQServer(1, 2, "fifo")

        server.add("sleep 3", 1)
        server.add("sleep 3", 1)
        server.add("sleep 3", 1)

        jobs = server.get_status_all()
        self.assertEqual(jobs, {1 : Status.PENDING, 2 : Status.PENDING, 3 : Status.PENDING})

    def test_shell_true(self):
        server = localq.LocalQServer(num_cores_available=2, interval=1,
                                     priority_method="fifo", use_shell=True)
        server.run()
            # localq.LocalQServer(1, 1, "fifo", use_shell=True)
        server.add("ls -la > /dev/null", 1, rundir="/tmp")
        assert server.get_status(1) == Status.PENDING
        time.sleep(2)
        assert server.get_status(1) == Status.COMPLETED

