import unittest

class TestLocalQServer(unittest.TestCase):
    def test_add(self):
        # self.assertEqual(expected, add(self, cmd, num_cores, rundir, stdout, stderr, name, dependencies))
        assert False # TODO: implement your test here

    def test_add_script(self):
        # self.assertEqual(expected, add_script(self, script, num_cores, rundir, stdout, stderr, name))
        assert False # TODO: implement your test here


    def test_get_new_jobid(self):
        # self.assertEqual(expected, get_new_jobid(self))
        assert False # TODO: implement your test here

    def test_get_status_all(self):
        # self.assertEqual(expected, get_status_all(self))
        assert False # TODO: implement your test here

    def test_list_queue(self):
        # self.assertEqual(expected, list_queue(self))
        assert False # TODO: implement your test here

    def test_jobs(self):
        # self.assertEqual(expected, jobs(self))
        assert False # TODO: implement your test here

    def test_get_status(self):
        # self.assertEqual(expected, get_status(self, jobid))
        assert False # TODO: implement your test here

    def test_get_job_with_id(self):
        # self.assertEqual(expected, get_job_with_id(self, jobid))
        assert False # TODO: implement your test here

    def test_stop_job_with_id(self):
        # self.assertEqual(expected, stop_job_with_id(self, jobid))
        assert False # TODO: implement your test here

    def test_stop_all_jobs(self):
        # self.assertEqual(expected, stop_all_jobs(self))
        assert False # TODO: implement your test here

    def test_run(self):
        # self.assertEqual(expected, run(self))
        assert False # TODO: implement your test here

    def test_wait(self):
        # self.assertEqual(expected, wait(self))
        assert False # TODO: implement your test here

    def test_get_server_cores(self):
        # self.assertEqual(expected, get_server_cores(self))
        assert False # TODO: implement your test here

    def test_write_dot(self):
        # self.assertEqual(expected, write_dot(self, f))
        assert False # TODO: implement your test here

    def test_get_ordered_jobs(self):
        # self.assertEqual(expected, get_ordered_jobs(self))
        assert False # TODO: implement your test here

    def test_get_runnable_jobs(self):
        # self.assertEqual(expected, get_runnable_jobs(self))
        assert False # TODO: implement your test here

    def test_get_node_with_name(self):
        # self.assertEqual(expected, get_node_with_name(self, name_to_find))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
