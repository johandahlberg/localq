# localq

`localq` is a job scheduler ment to be run on a single node. Jobs can be submitted to it, which are then run when resources are available. 

# Installation

```bash
git clone https://github.com/dakl/localq.git
pip install -r localtq/requirements.txt ./localq
```

# Testing

```bash
cd localq
py.test
```

# TL;DR.

To start a server with 2 core available for jobs, polling the queue every 10 seconds, run
 
```bash
localqserver_start -n 2 -i 10 &
```

Jobs can now be submitted to this server: 

```bash
lbatch ls
lbatch sh my_script.sh
lbatch -n 2 echo "my two-core job"
```

To list all jobs, use `lqueue`: 

```bash
lqueue
```

To get the status of a single job, use `linfo`:

```bash
linfo -j 1
```

To cancel a job, use `lcancel`:

```bash
lcancel -j 1
```


When you're done, the server should be stopped:

```bash
localqserver_wait
```

`localqserver_wait` will wait until all jobs submitted to the server are completed and then kill it.

# Launching the localqd server

To start a server with 8 cores available for jobs, polling the queue every 15 seconds, run 

```bash
localqserver_start -n 8 -i 15 -u ~/tmp/mysecondserver &
```

This will create a file containing the server URI (`~/tmp/mysecondserver `). Since the URI is written to a file, the user can create an arbitrary number of separate queues by setting separate URI files for each instance of `localqserver_start`.

# Submitting jobs

Jobs are submitted to localq using `lbatch`

```bash
lbatch -n 1 -u ~/tmp/mysecondserver ls -lah
lbatch -n 1 -u ~/tmp/mysecondserver hostname
lbatch -n 2 -u ~/tmp/mysecondserver echo "Two Core Job"
lbatch -n 2 -u ~/tmp/mysecondserver -o my-twocore-job-logfile.txt echo "Two Core Job with log"
localqserver_wait
```

Parameters:

```
Options:
  -n N        number of cores to use.
  -o STDOUT   file for stdout
  -u URIFILE  file where the uri for the localqd is written
```

If `-o` is not set on the command line, output from the job will be written to `localq-[JOBID]-[SUBMITTED_DATETIME].out`.

# Security

LocalQ uses Pyro4 to communicate between the client(s) (`lbatch`, `linfo`, `lqueue`, `lcancel`) and the server started by `localqserver_start`. This is done by writing to Pyro4 URI to a file specified by the parameter `-u` which is given user-only readability to protect it so that the only the user who launched the server can submit jobs to it.

# Resource monitoring

LocalQ does not monitor resources used by each job, which is the responsability of the user. This means that it's possible to submit a job and tell LocalQ to use two cores

```bash
lbatch -n 1 bwa mem -t 16 ref.fa input.fq.gz
```

In the example above, `lbatch` is instructed to submit a two-core job to the queue, but the job itself is instructed to use 16 cores (`bwa ... -t 16 ...`). This will not cause LocalQ to fail, and needs to be handled by the user.

# TODO

* Settable strategy to prioritize jobs when launching localqd
 * [x] `fifo` = First come, first serve
 * [ ] `mcf` = Prioritize jobs with largest number of requested cores highest
* [x] `linfo -j 123`
* [x] `lcancel -j 123`
