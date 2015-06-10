# localq

`localq` is a job scheduler ment to be run on a single node. Jobs can be submitted to it, which are then run when resources are available. 

#Prerequsites

* Pyro4 python module (`pip install Pyro4`)

# TL;DR.

To start a server with 1 core available for jobs, polling the queue every 30 seconds, run
 
```bash
localqd start
```

Jobs can now be submitted to this server: 

```bash
lbatch ls
lbatch sh my_script.sh
```

To list the jobs, use `lqueue`: 

```bash
lqueue
```

When you're done, the server daemon should be stopped: 

```bash
localqd stop
```

# Launching the localqd daemon

To start a server with 8 cores available for jobs, polling the queue every 15 seconds, run 

```bash
localqd -n 8 -i 15 -u ~/tmp/mysecondserver start
```

This will create a file containing the server URI (`~/tmp/mysecondserver `) and a file containing the servers PID (`~/tmp/mysecondserver.pid`). Since the URI is written to a file, the user can create an arbitrary number of separate queues by setting separate URI files for each instance of `localqd`. 

# Submitting jobs

Jobs are submitted to localq using `lbatch`

```bash
python lbatch -n 1 -u ~/tmp/mysecondserver ls -lah
python lbatch -n 1 -u ~/tmp/mysecondserver hostname
python lbatch -n 2 -u ~/tmp/mysecondserver echo "Two Core Job"
```

The flag `-n` specifies the number of cores requested for the job (default `1` if omitted). The rest is the command that will be executed by `localqd.py`

# TODO

* Settable strategy to prioritize jobs when launching localqd
 * [x] `fifo` = First come, first serve
 * [ ] `mcf` = Prioritize jobs with largest number of requested cores highest
* `linfo -j 123`
* `lcancel -j 123`
