__author__ = 'dankle'

import unittest

from random import shuffle

from localq.job import Job
from localq.job_prioritizer import JobPrioritizer as Prioritizer


class TestJobPrioritizer(unittest.TestCase):

    job1 = Job(1, "echo", num_cores=1)
    job2 = Job(2, "echo", num_cores=2)
    job3 = Job(3, "echo", num_cores=3)

    job_list = [job1, job2, job3]
    # Ensure the list is randomly sorted - as to
    # avoid problems with accidentally getting the
    # correct element with top priority.
    shuffle(job_list)

    def test_fifo(self):
        sorted_list = Prioritizer.fifo(self.job_list)
        assert sorted_list[0] == self.job1

    def test_max_cores_first(self):
        sorted_list = Prioritizer.max_cores_first(self.job_list)
        print sorted_list[0]
        assert sorted_list[0] == self.job3

    if __name__ == '__main__':
        unittest.main()
