import unittest
from localq.LocalQServer import LocalQServer
from localq.Job import Job
from localq.Status import Status
from mock import patch, MagicMock
import networkx
import time


class TestLocalQServer(unittest.TestCase):

    server = None
    cmd = ["ls", "-la"]

    def setUp(self):
        self.server = LocalQServer(num_cores_available=2, interval=1, priority_method="fifo", use_shell=True)

    def add_some_jobs(self):
        for i in range(0, 4):
            self.server.add(cmd=self.cmd, num_cores=1)

    def add_some_jobs_with_dependencies(self):
        for i in range(1, 5):
            if i > 1:
                self.server.add(cmd=self.cmd, num_cores=1, dependencies=[i-1])
            else:
                self.server.add(cmd=self.cmd, num_cores=1)

    def test_add(self):
        # To many cores
        job_id = self.server.add(cmd=self.cmd, num_cores=3)
        assert not job_id
        assert not filter(lambda x: x.jobid, self.server.graph.nodes())

        job_id = self.server.add(cmd=self.cmd, num_cores=1)
        assert filter(lambda x: x.jobid, self.server.graph.nodes())
        assert isinstance(job_id, int)

    def test_add_script(self):
        # self.assertEqual(expected, add_script(self, script, num_cores, rundir, stdout, stderr, name))
        job_id = self.server.add_script(script=self.cmd, num_cores=1)
        assert filter(lambda x: x.jobid, self.server.graph.nodes())
        assert isinstance(job_id, int)

    def test_get_status_all(self):
        expected_status = {1: 'PENDING', 2: 'PENDING', 3: 'PENDING', 4: 'PENDING'}
        self.add_some_jobs()
        assert self.server.get_status_all() == expected_status

    def test_list_queue(self):
        # self.assertEqual(expected, list_queue(self))
        self.add_some_jobs()
        actual_queue = self.server.list_queue()

        # This just duplicated the real code.
        # At least it protects against unexpected regression.
        expected_str = "\t".join(["JOBID", "PRIO", "STATUS", "NUM_CORES", "START_TIME", "END_TIME", "NAME", "CMD", "\n"])
        for j in self.server.jobs():
            expected_str += j.info() + "\n"
        expected_str = expected_str.strip("\n")

        self.assertEqual(actual_queue, expected_str)

    def test_jobs(self):
        self.add_some_jobs()
        self.assertEqual(self.server.graph.nodes(), self.server.jobs())

    def test_get_status(self):
        self.add_some_jobs()
        expected_status = Status.PENDING
        self.assertEqual(expected_status, self.server.get_status(1))

    def test_get_job_with_id(self):
        self.add_some_jobs()
        actual_job = self.server.get_job_with_id(1)
        self.assertEqual(actual_job.jobid, 1)

        job_not_there = self.server.get_job_with_id(111)
        self.assertEqual(job_not_there, None)

    def test_stop_job_with_id(self):
        with patch.object(Job, "kill", return_value=None) as mock_kill:
            self.add_some_jobs()
            result = self.server.stop_job_with_id(1)
            self.assertEqual(1, result)
            mock_kill.assert_called_with()

            # Try to kill job that doesn't exist
            result = self.server.stop_job_with_id(111)
            self.assertEqual(None, result)

    def test_stop_all_jobs(self):
        with patch.object(Job, "kill", return_value=None) as mock_kill:
            self.add_some_jobs()
            self.server.stop_all_jobs()
            self.assertEqual(mock_kill.call_count, 4)

    def test_run(self):
        mock_job = MagicMock()
        mock_job.run = MagicMock()
        mock_job.num_cores = 1
        with patch.object(LocalQServer, "get_runnable_jobs", side_effect=[[mock_job], []]):
            self.server.run()
            # Since run will spawn it's own thread we need to
            # wait a while here to make sure run has been called
            time.sleep(1)
            self.assertEqual(mock_job.run.call_count, 1)

    def test_wait(self):
        mock_return = MagicMock()
        mock_return.side_effect = [{1: 'PENDING', 2: 'PENDING'}, {1: 'COMPLETE', 2: 'COMPLETE'}]
        self.server.get_status_all = mock_return
        self.server.wait()
        self.assertEqual(mock_return.call_count, 2)

    def test_get_server_cores(self):
        self.assertEqual(self.server.get_server_cores(), self.server.num_cores_available)

    def test_write_dot(self):
        with patch.object(networkx, "write_dot", return_value=None) as mock_write_dot:
            self.server.write_dot("/foo")
            mock_write_dot.assert_called_with(self.server.graph, "/foo")

    def test_get_ordered_jobs(self):
        self.add_some_jobs()
        with patch.object(networkx, "is_directed_acyclic_graph", return_value=False):
            with self.assertRaises(Exception):
                self.server.get_ordered_jobs()

        with patch.object(networkx, "is_directed_acyclic_graph", return_value=True), \
             patch.object(networkx, "topological_sort", return_value="foo"):
            result = self.server.get_ordered_jobs()
            self.assertEqual(result, "foo")

    def test_get_runnable_jobs(self):
        self.add_some_jobs_with_dependencies()
        self.assertEqual(len(self.server.get_runnable_jobs()), 1)
        self.assertEqual(self.server.get_runnable_jobs()[0].jobid, 1)

    def test_get_node_with_name(self):
        self.add_some_jobs()
        result = self.server.get_node_with_name("localq-1")
        self.assertEqual(result.jobid, 1)

if __name__ == '__main__':
    unittest.main()
