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
        self.queue = []
        self.running = []
        self.completed = []
        self.next_jobid = 1

    def add(self, cmd, num_cores, rundir=None):
        job = localq.Job(cmd, num_cores, stdout=self.stdout, stderr=self.stderr, rundir=rundir)
        self.queue.append(job)
        job.set_jobid(self.next_jobid)
        self.next_jobid += 1
        return job.jobid

    def list_queue(self):
        retstr = ""
        retstr += "JOBID\tPRIO\tSTATUS\tNUM_CORES\tPRIO_METHOD\tCMD\n"
        for j in self.running:
            retstr += j.info() + "\n"
        for j in self.queue:
            retstr += j.info() + "\n"
        for j in self.completed:
            retstr += j.info() + "\n"
        return retstr.strip("\n")


    def run(self):
        print "Starting localqd with {} available cores".format(self.num_cores_available)
        print "Checking queue every {} seconds".format(self.interval)

        def check_queue():
            while True:

                # check which running jobs are completed
                for job in self.running:
                    if job.status() == localq.Job.COMPLETED or job.status() == localq.Job.FAILED:
                        self.running.remove(job)
                        self.completed.append(job)
                    else:  # if job is still running, or has failed
                        pass

                sortedqueue = sorted(self.queue, key=methodcaller('priority'), reverse=True)

                # check if new jobs can be started
                for job in sortedqueue:
                    n_cores_busy = 0
                    for j in self.running:
                        n_cores_busy += j.num_cores
                    cores_available = self.num_cores_available - n_cores_busy

                    if cores_available >= job.num_cores:
                        job.run()
                        self.running.append(job)
                        self.queue.remove(job)
                    else:  # If highest-priority job can't start, don't try to start next job until next cycle
                        continue

                time.sleep(self.interval)

        thread = threading.Thread(target=check_queue)
        thread.setDaemon(True)
        thread.start()
