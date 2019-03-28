This allows you to submit `plot.py` to the batch system,
plotting one variable per region per core for parallelised plotting.

First, make the batch submission scripts by running 
(opening this to configure paths accordingly)
```
make_batch_scripts.py
```

Then open and configure the `send_plotting_to_batch.py` script
with what variables and regions you want
Then run this script to send to the batch to plot:
```
./send_plotting_to_batch.py
```
