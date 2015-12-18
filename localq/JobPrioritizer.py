

@staticmethod
def fifo(pending_jobs, **kwargs):
    """
    Perform first in first out prioritizing
    :param pending_jobs:
    :return:
    """
    def _priority_by_job_id(job):
        return -1 * job.jobid

    return sorted(pending_jobs, key=_priority_by_job_id, reverse=True)

@staticmethod
def max_nbr_cores_engaged(pending_jobs):
    pass

@staticmethod
def max_cores_first(pending_jobs):
    pass
