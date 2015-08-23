__author__ = 'dankle'

import unittest
import subprocess

from mock import MagicMock, patch
from localq.Status import Status

from localq.Job import Job

class TestJob(unittest.TestCase):

    unique_job_id = 0
    job = None

    def setUp(self):
        self.unique_job_id += 1
        cmd = ["ls", "-la"]
        self.job = Job(self.unique_job_id, cmd)

    def test__hash__(self):
        self.assertEqual(self.job_id, self.job.__hash__())

    def test___init__(self):
        # only check name is correctly set if no name specified.
        assert self.job.name == "localq-" + str(self.job_id)

    def test___str__(self):
        expected = str(self.job.jobid) + "-" + str(self.job.name)
        self.assertEqual(expected, self.job.__str__())

    def test_info(self):
        expected = "\t".join(
            [str(self.job.jobid),
             str(self.job.priority()),
             str(self.job.status()),
             str(self.job.num_cores),
             str(self.job.start_time),
             str(self.job.end_time),
             str(self.job.name),
             str(" ".join(self.job.cmd))]
        )
        self.assertEqual(expected, self.job.info())

    def test_kill(self):
        self.job.proc = MagicMock()
        self.job.kill()
        self.job.proc.kill.assert_called_with()
        assert self.job._status == Status.CANCELLED

        self.job.proc.kill = MagicMock(side_effect=OSError("foo"))
        self.job.kill()
        self.job.proc.kill.assert_called_with()
        assert self.job._status == Status.CANCELLED


    def test_priority(self):
        self.assertEqual(-1 * self.job_id, self.job.priority())

    def test_run(self):
        with patch.object(subprocess, "Popen", return_value="Fake process"):
            # Should just run without trouble.
            self.job.run()
            assert self.job.proc == "Fake process"
        # if an exception is thrown, make sure it's handled.
        with patch.object(subprocess, "Popen", side_effect=OSError("foo")):
            self.job.run()
            assert self.job.proc == None
            assert self.job._failed_to_start

    def test_status(self):
        with patch.object(Job, "update_status", return_value=None) as mock_update_status:
            actual_status = self.job.status()
            mock_update_status.assert_called_with()
            assert self.job._status == actual_status

    def test_update_status(self):
        mock_proc = MagicMock(returncode=None)
        self.job.proc = mock_proc

        self.job._status = Status.CANCELLED
        self.job.update_status()
        assert self.job._status == Status.CANCELLED

        self.job._status = Status.RUNNING
        mock_proc = MagicMock(returncode=None)
        self.job.proc = mock_proc
        self.job.update_status()
        assert self.job._status == Status.RUNNING

        self.job._status = Status.RUNNING
        mock_proc = MagicMock(returncode=-1)
        self.job.proc = mock_proc
        self.job.update_status()
        assert self.job._status == Status.CANCELLED

        self.job._status = Status.RUNNING
        mock_proc = MagicMock(returncode=1)
        self.job.proc = mock_proc
        self.job.update_status()
        assert self.job._status == Status.FAILED

        self.job.proc = False
        self.job.update_status()
        assert self.job._status == Status.PENDING

        self.job._failed_to_start = True
        self.job.update_status()
        assert self.job._status == Status.FAILED


    if __name__ == '__main__':
        unittest.main()