"""
LocalQServer
"""

import time
import threading
import localq
from operator import methodcaller


class LocalQServer():
    def __init__(self, num_cores_available, interval, priority_method, stderr="/dev/null", stdout="/dev/null"):
        self.num_cores_available = num_cores_available
        self.interval = float(interval)
        self.priority_method = priority_method
        self.stdout = stdout
        self.stderr = stderr
        self.pending = []
        self.running = []
        self.completed = []
        self.failed = []
        self.next_jobid = 1

    def add(self, cmd, num_cores, rundir=None, stdout=None, stderr=None):
        job = localq.Job(cmd, num_cores, stdout=stdout, stderr=stderr, rundir=rundir)
        job.set_jobid(self.next_jobid)
        self.pending.append(job)
        self.next_jobid += 1
        return job.jobid

    def list_queue(self):
        retstr = ""
        retstr += "JOBID\tPRIO\tSTATUS\tNUM_CORES\tPRIO_METHOD\tCMD\n"
        for j in self.running:
            retstr += j.info() + "\n"
        for j in self.pending:
            retstr += j.info() + "\n"
        for j in self.completed:
            retstr += j.info() + "\n"
        for j in self.failed:
            retstr += j.info() + "\n"
        return retstr.strip("\n")

    def get_status(self, jobid):
        """
        Check in which state (list) a job is.
        Jobs are moved between lists every self.interval seconds (see LocalQServer.run() for implementation)
        :param jobid: a job id to search for
        :return: Any of Job.PENDING, RUNNING, COMPLETED or FAILED. If no job with the given ID is found, None is returned.
        """
        if jobid in [j.jobid for j in self.pending]:
            return localq.Job.PENDING
        if jobid in [j.jobid for j in self.running]:
            return localq.Job.RUNNING
        if jobid in [j.jobid for j in self.completed]:
            return localq.Job.COMPLETED
        if jobid in [j.jobid for j in self.failed]:
            return localq.Job.FAILED
        else:
            return None

    def stop_job_with_id(self, jobid):
        """
        stop a job with a give ID
        :param jobid: Job ID of job to stop
        :return: the jobs
        """
        retval = 0
        for j in self.running:
            retval = j.kill()
        for j in self.pending:
            retval = j.kill()
        for j in self.completed:
            pass
        for j in self.failed:
            pass
        return retval

    def run(self):
        print "Starting localqd with {} available cores".format(self.num_cores_available)
        print "Checking queue every {} seconds".format(self.interval)

        def check_queue():
            while True:

                # check which running jobs are completed
                for job in self.running:
                    # if job is completed, move to self.completed
                    if job.status() == localq.Job.COMPLETED:
                        self.running.remove(job)
                        self.completed.append(job)

                    # if job failed, move to self.failed
                    elif job.status() == localq.Job.FAILED:
                        self.running.remove(job)
                        self.failed.append(job)
                    else:  # if job is still running, keep it in self.running
                        pass

                sortedqueue = sorted(self.pending, key=methodcaller('priority'), reverse=True)

                # check if new jobs can be started
                for job in sortedqueue:
                    n_cores_busy = 0
                    for j in self.running:
                        n_cores_busy += j.num_cores
                    cores_available = self.num_cores_available - n_cores_busy

                    if cores_available >= job.num_cores:
                        job.run()
                        self.running.append(job)
                        self.pending.remove(job)
                    else:  # If highest-priority job can't start, don't try to start next job until next cycle
                        continue

                time.sleep(self.interval)

        thread = threading.Thread(target=check_queue)
        thread.setDaemon(True)
        thread.start()

    def get_server_cores(self):
        """
        :return: Number of cores available to the server
        """
        return self.num_cores_available

