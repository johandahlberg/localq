import Pyro4
import time
import threading
import Job

#import time
#from Job import Job

__author__ = 'dankle'

class LocalQServer():
    def __init__(self, num_cores_available):
        self.num_cores_available = num_cores_available
        self.joblist = []
        self.running = []
        self.next_jobid = 1

    def joke(self, name):
        return "Sorry "+name+", I don't know any jokes."

    def add(self, cmd, num_cores):
        job = Job.Job(cmd, num_cores)
        self.joblist.append(job)
        job.set_jobid(self.next_jobid)
        self.next_jobid += 1
        #print "Queue len after adding " + str(cmd) + "/n=" + str(num_cores) + ": " + str(len(self.joblist))
        return job.jobid

    def run(self):
        print "Starting localqd with {} available cores".format(self.num_cores_available)
        def check_queue():
            while True:
                print "Queue length = " + str(len(self.joblist))
                for job in self.joblist:
                    job.run()
                    self.joblist.remove(job)
                time.sleep(5)

        thread = threading.Thread(target=check_queue)
        thread.setDaemon(True)
        thread.start()



import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument('-n', help="Number of available cores", action="store", required=False, default=1)
opts = ap.parse_args()

daemon = Pyro4.Daemon()
localqserver = LocalQServer(opts.n)
uri = daemon.register(localqserver)

ns = Pyro4.locateNS()
ns.register("localqd", uri)

localqserver.run()

daemon.requestLoop()

