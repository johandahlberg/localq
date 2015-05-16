"""
LocalQServer

# create a server with 8 available cores
server = LocalQServer(8)
# start the server
server.run()

Add jobs to the server

server.add()
"""

import time
import threading
import Job

class LocalQServer():
    def __init__(self, num_cores_available, interval):
        self.num_cores_available = num_cores_available
        self.interval = interval
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
        print "Checking queue every {} seconds".format(self.interval)
        def check_queue():
            while True:
                print "Queue length = " + str(len(self.joblist))
                for job in self.joblist:
                    job.run()
                    self.joblist.remove(job)
                time.sleep( float(self.interval) )

        thread = threading.Thread(target=check_queue)
        thread.setDaemon(True)
        thread.start()
