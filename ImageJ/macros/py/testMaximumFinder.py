# testMaximumFinder.py
# translated to Jython by J. R. Minter based upon a JavaScript example
# by Wayne Rasband.
# It uses the MaximumFinder.getMaxima() method, which returns the list of x,y
# coordinates as a Polygon.
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2015-01-23  JRM 0.1.00  Initial translation
# 
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
from ij.plugin.filter import MaximumFinder

tolerance = 50
excludeOnEdges = False
img = IJ.openImage("http://imagej.nih.gov/ij/images/blobs.gif")
ip = img.getProcessor()
mf = MaximumFinder()
maxima = mf.getMaxima(ip, tolerance, excludeOnEdges)
print("count = %d" % maxima.npoints)