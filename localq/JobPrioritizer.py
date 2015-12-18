

@staticmethod
def fifo(pending_jobs, **kwargs):
    """
    Perform first in first out prioritizing
    :param pending_jobs:
    :return:
    """
    def priority_by_job_id(job):
        return -1 * job.jobid

    return sorted(pending_jobs, key=priority_by_job_id, reverse=True)

@staticmethod
def max_nbr_cores_engaged(pending_jobs, **kwargs):
    pass

@staticmethod
def max_cores_first(pending_jobs, **kwargs):
    def priority_by_cores_used(job):
        return -1 * job.num_cores
    return sorted(pending_jobs, key=priority_by_cores_used, reverse=True)
