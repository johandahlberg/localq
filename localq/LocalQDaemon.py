__author__ = 'dankle'

import Pyro4
import localq
import sys
import os


class LocalQDaemon(localq.Daemon):

    def __init__(self, num_cores, interval, urifile, priority_method):
        self.pyrodaemon = None
        self.uri = None
        self.localqserver = None
        self.daemon = None
        self.num_cores = num_cores
        self.interval = interval
        self.urifile = urifile
        self.priority_method = priority_method
        pidfile = urifile + ".pid"
        localq.Daemon.__init__(self, pidfile)
        self.localq_stdout = urifile + ".stdout.txt"
        self.localq_stderr = urifile + ".stderr.txt"

    def stop(self):
        # First, kill all jobs
        try:
            pf = file(self.urifile,'r')
            uri = str(pf.read().strip())
            pf.close()
        except IOError:
            uri = None

        if not uri:
            message = "urifile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.urifile)
            return  # not an error in a restart
        else:
            os.remove(self.urifile)
            localqd = Pyro4.Proxy(uri)
            #localqd.stop_all_jobs()

        # Finally, run the
        localq.Daemon.stop(self)

    def run(self):
        self.pyrodaemon = Pyro4.core.Daemon()
        self.localqserver = localq.LocalQServer(self.num_cores, self.interval, self.priority_method)
        self.uri = self.pyrodaemon.register(self.localqserver)

        # Check for a urifile to see if the daemon already runs
        try:
            pf = file(self.urifile, 'r')
            uri_on_disk = str(pf.read().strip())
            pf.close()
        except IOError:
            uri_on_disk = None

        if uri_on_disk:
            message = "urifile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.urifile)
            sys.exit(1)

        file(self.urifile,'w+').write("%s\n" % self.uri)
        import stat
        os.chmod(self.urifile, stat.S_IRUSR)

        print(self.uri)
        print(self.urifile)
        print(self.pidfile)

        self.localqserver.run()
        self.pyrodaemon.requestLoop()
