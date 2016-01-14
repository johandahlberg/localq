

class JobPrioritizer:

    def __init__(self):
        pass

    @staticmethod
    def fifo(pending_jobs, **kwargs):
        """
        Perform first in first out prioritizing
        :param pending_jobs: list of jobs to prioritize
        :return: the list of jobs sorted by priority
        """
        def priority_by_job_id(job):
            return -1 * job.jobid

        return sorted(pending_jobs, key=priority_by_job_id, reverse=True)

    @staticmethod
    def max_cores_first(pending_jobs, **kwargs):
        """
        Run jobs with the maximum number of cores used first.
        :param pending_jobs: list of jobs to prioritize
        :param kwargs: list of jobs sorted by cores used.
        :return:
        """
        def priority_by_cores_used(job):
            return -1 * job.num_cores
        return sorted(pending_jobs, key=priority_by_cores_used)
