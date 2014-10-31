# testAutomateDialog.py
# Run a thread
# adapted from http://albert.rierol.net/imagej_programming_tutorials.html#How to automate an ImageJ dialog
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-15  JRM 0.1.00  Get'er done

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
from ij import Macro
from java.lang import Thread

# Prepare options for Bandpass filter
options = "filter_large=40 filter_small=3 suppress=None tolerance=5 autoscale saturate"
# Get the current thread
thread = Thread.currentThread()
original_name = thread.getName()
# Rename current thread
thread.setName("Run$_my_batch_process")
# Set the options for the current thread
Macro.setOptions(Thread.currentThread(), options)

# Get the current image
imp = IJ.getImage();
# Finally, run the bandpass filter without dialogs:
IJ.runPlugIn(imp, "ij.plugin.filter.FFTFilter", "")

# Be nice: undo naming, so other scripts may run with dialogs
thread.setName(original_name);
# Be safe: remove the thread's options from the table
# (which also removes the reference to the thread itself)
Macro.setOptions(thread, None)
