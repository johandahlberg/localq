"""
LocalQServer
"""

import time
import threading
import localq
from operator import methodcaller
from localq.Status import Status

class LocalQServer():
    def __init__(self, num_cores_available, interval, priority_method):
        self.num_cores_available = int(num_cores_available)
        self.interval = float(interval)
        self.priority_method = priority_method
        self.jobs = []
        self._last_jobid = 0

    def add(self, cmd, num_cores, rundir=None, stdout=None, stderr=None, name=None):
        job = localq.Job(cmd, num_cores, stdout=stdout, stderr=stderr, rundir=rundir, name=name)
        # if number of requested cores is bigger then the number of cores available to the system, fail submission.
        if job.num_cores > self.num_cores_available:
            return None
        else:
            job.set_jobid(self.get_new_jobid())
            self.jobs.append(job)
            return job.jobid

    def add_script(self, script, num_cores, rundir, stdout, stderr, name):
        cmd = ["sh", script]
        return self.add(cmd, num_cores, stdout=stdout, stderr=stderr, rundir=rundir, name=name)

    def get_new_jobid(self):
        """
        Method to get a new jobid to use for a job. Increments internal jobid tracker variable each time it's called.
        :return: a job id (int)
        """
        self._last_jobid += 1
        return self._last_jobid

    def get_status_all(self):
        """
        Get the status of all know jobs.
        :return: a dict with job-ids as keys, and their status as values.
        """
        jobs_and_status = map(lambda job: (job.jobid, job.status()), self.jobs)
        print(jobs_and_status)
        return dict(jobs_and_status)

    def list_queue(self):
        retstr = "JOBID\tPRIO\tSTATUS\tNUM_CORES\tSTART_TIME\tEND_TIME\tNAME\tCMD\n"
        for j in self.jobs:
            retstr += j.info() + "\n"
        return retstr.strip("\n")

    def get_status(self, jobid):
        """
        Check in which state (list) a job is.
        :param jobid: a job id to search for
        :return: Any of Status.PENDING, RUNNING, COMPLETED or FAILED.
        If no job with the given ID is found, Status.NOT_FOUND is returned.
        """
        job = self.get_job_with_id(int(jobid))
        if job:
            return job.status()
        else:
            return Status.NOT_FOUND

    def get_job_with_id(self, jobid):
        jobs = [job for job in self.jobs if job.jobid == jobid]
        if len(jobs) > 0:
            return jobs[0]
        else:
            return None

    def stop_job_with_id(self, jobid):
        """
        stop a job with a give ID
        :param jobid: Job ID of job to stop
        :return: the jobs new ID after it was tried to be stopped (None if it can not find the job)
        """
        job = self.get_job_with_id(int(jobid))
        if job:
            job.kill()
            return jobid
        else:
            return None

    def stop_all_jobs(self):
        for job in self.jobs:
            print "Sending SIGKILL to " + str(job.jobid)
            job.kill()

    def run(self):
        print "Starting localqd with {} available cores".format(self.num_cores_available)
        print "Checking queue every {} seconds".format(self.interval)

        def get_n_cores_booked():
            n_cores_booked = 0
            running_jobs = [j for j in self.jobs if j.status() == Status.RUNNING]
            for job in running_jobs:
                n_cores_booked += job.num_cores
            return n_cores_booked

        def check_queue():
            while True:
                pending_jobs = [j for j in self.jobs if j.status() == Status.PENDING]
                pending_jobs = sorted(pending_jobs, key=methodcaller('priority'), reverse=True)

                # check if new jobs can be started
                for job in pending_jobs:
                    n_cores_busy = get_n_cores_booked()
                    cores_idle = self.num_cores_available - n_cores_busy
                    if cores_idle >= job.num_cores:
                        job.run()
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

