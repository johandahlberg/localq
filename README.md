# localq

`localq` is a job scheduler ment to be run on a single node. Jobs can be submitted to it, which are then run when resources are available. 

#Prerequsites

* Pyro4 python module (`pip install Pyro4`)

# Launching the localqd server

Launching the server is a two-step procedures. First, the Pyro4 name server needs to be started:

```bash
pyro4-ns -n localhost &
```

Then, `localqd` can be started:

```bash
python localqd.py -n 4 > log.txt 2>&1 &
```

The flag `-n` specifies the number of cores available to submitted jobs. 

# Submitting jobs

Jobs are submitted to localq using `lbatch.py`

```bash
python lbatch.py -n 1 ls -lah
python lbatch.py -n 1 hostname
python lbatch.py -n 2 echo "Two Core Job"
```

The flag `-n` specifies the number of cores requested for the job (default `1` if omitted). The rest is the command that will be executed by `localqd.py`

# TODO

* Daemonize the server 
 * syntax `python localqd.py [start|stop|restart] `
* Settable strategy to prioritize jobs when launching localqd
 * `fcfs` = First come, first serve
 * `mcf` = Prioritize jobs with largest number of requested cores highest
 * `python localqd.py -s [fcfs|mcf|...] [start|stop|restart] `

