# gadgetron-python-demo
for fun and runable

# prepare env (prefer in mini conda)
```bash
pip install gadgetron gadgetron-dataflow-monitor ismrmrdviewer
```

# start gadgetron first
```bash
gadgetron
```

# demo time

## full recon by python (from gadgetron-python)
```bash
gadgetron_ismrmrd_client -f testdata.h5 -C gadgetron_python_sample.xml
ismrmrdviewer out.h5
```
## passthrough
```bash
gadgetron_ismrmrd_client -f testdata.h5 -C passthough_demo.xml
```
## datflow monitor
```bash
gadgetron_ismrmrd_client -f testdata.h5 -C dataflow_monitor.xml
```
## plot image and save
```bash
gadgetron_ismrmrd_client -f testdata.h5 -C plotsave_demo.xml
ismrmrdviewer out.h5
```
## dataflow monitor and plot image and save
```bash
gadgetron_ismrmrd_client -f testdata.h5 -C dataflow_monitor_plotsave_demo.xml
ismrmrdviewer out.h5
```

# python debug tips
if you want to debug you python, you can start your python youself, and tell gadgetron to connect to it like:

```bash
python  plotsave_demo.py # you can start anywhere like debug in Pycharm 
gadgetron_ismrmrd_client -f testdata.h5 -C plotsave_demo_start_by_hand.xml
ismrmrdviewer out.h5
```