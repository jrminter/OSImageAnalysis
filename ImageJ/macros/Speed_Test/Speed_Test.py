"""
Sphere.py

A speed test example fixed

                     Modifications
  Date      Who  Ver                       What
----------  --- ------  -------------------------------------------------
2017-04-02  JRM 0.1.00  Initial test with 4096. Original example did not
                        import functions. 11.594sec on jrmFastMac
"""

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from java.lang import System
from ij import IJ, ImagePlus
from ij.process import FloatProcessor
from math import sqrt


t0 = System.currentTimeMillis()
size = 4096
ip = FloatProcessor(size,size)
for y in range(size):
   IJ.showProgress(y,size-1)
   for x in range(size):
       dx=x-size/2; dy=y-size/2
       d = sqrt(dx*dx+dy*dy)
       ip.setf(x,y,-d)
time = str((System.currentTimeMillis()-t0)/1000.0)+" seconds"
ImagePlus(time,ip).show()
IJ.run("Red/Green");