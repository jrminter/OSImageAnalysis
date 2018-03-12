"""
setStandardOptions.py

Set standard options recommended by Cameron Nowell in the Monash University
Training Notes (June, 2016). 

  Modifications
   Date      Who  Ver                       What
----------  --- ------  -------------------------------------------------
2018-02-22  JRM 0.1.00  Initial set
"""
from ij import IJ

print("Setting standard options")

IJ.run("Memory & Threads...", "maximum=9830 parallel=4");
IJ.run("Colors...", "foreground=white background=black selection=yellow")
IJ.run("Options...", "iterations=1 count=1 black pad")

print("Done")
