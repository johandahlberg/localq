__author__ = 'dankle'

import unittest
from localq.Job import Job

class TestJob(unittest.TestCase):

    # def test_job(self):
    #     job = localq.Job(["ls", "-la"], num_cores=1, name="testjob")
    #     job.set_jobid(1)
    #     assert job.num_cores == 1
    #     assert job.cmd == ["ls", "-la"]
    #     assert job.jobid == 1
    #     assert job.status() == Status.PENDING
    #     assert job.priority_method == "fifo"
    #     assert job.priority() == -1
    #     assert job.name == "testjob"
    #     job.kill()
    #     assert job.status() == Status.CANCELLED
    #
    #     job_with_shell_true = localq.Job("ls -la > /dev/null", num_cores=1, name="testjob_with_shell_true", use_shell=True)
    #     job_with_shell_true.set_jobid(1)
    #     assert job_with_shell_true.num_cores == 1
    #     assert job_with_shell_true.cmd == "ls -la > /dev/null"
    #     assert job_with_shell_true.jobid == 1
    #     assert job_with_shell_true.status() == Status.PENDING
    #     assert job_with_shell_true.priority_method == "fifo"
    #     assert job_with_shell_true.priority() == -1
    #     assert job_with_shell_true.name == "testjob_with_shell_true"
    #     job_with_shell_true.kill()
    #     assert job_with_shell_true.status() == Status.CANCELLED


    job_id = 1
    cmd = ["ls", "-la"]
    job = Job(job_id, cmd)

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
        # job = Job(cmd, num_cores, stdout, stderr, priority_method, rundir, name, use_shell, dependencies)
        # self.assertEqual(expected, job.kill())
        assert False # TODO: implement your test here

    def test_priority(self):
        self.assertEqual(-1 * self.job_id, self.job.priority())

    def test_run(self):
        # job = Job(cmd, num_cores, stdout, stderr, priority_method, rundir, name, use_shell, dependencies)
        # self.assertEqual(expected, job.run())
        assert False # TODO: implement your test here

    def test_status(self):
        # job = Job(cmd, num_cores, stdout, stderr, priority_method, rundir, name, use_shell, dependencies)
        # self.assertEqual(expected, job.status())
        assert False # TODO: implement your test here

    def test_update_status(self):
        # job = Job(cmd, num_cores, stdout, stderr, priority_method, rundir, name, use_shell, dependencies)
        # self.assertEqual(expected, job.update_status())
        assert False # TODO: implement your test here

    if __name__ == '__main__':
        unittest.main()