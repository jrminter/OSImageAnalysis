# Curve fitting example
# see class CurveFitter
# http://rsb.info.nih.gov/ij/developer/api/ij/measure/CurveFitter.html
# 20110412 Kota
# 2014-11-02 JRM cvt to Jython and aded plot

from ij import IJ
from ij.measure import CurveFitter
from ij.gui import Plot


# create example data arrays
xa = [1., 2., 3., 4.]
ya = [3., 3.5, 4., 4.5];

# construct a CurveFitter instance
cf = CurveFitter(xa, ya);

# actual fitting
# fit models: see http://rsb.info.nih.gov/ij/developer/api/constant-values.html#ij.measure.CurveFitter.STRAIGHT_LINE
cf.doFit(CurveFitter.STRAIGHT_LINE);

# print out fitted parameters.

b = cf.getParams()[0]
m = cf.getParams()[1]

strOut = str(b) + " : " + str(m)

IJ.log(strOut);

xb = [0 ,5]
yb = [b, 5*m+b]

pl = Plot("Data", "x", "y")
pl.setLimits(0,5,0,5)
pl.addPoints(xa, ya, Plot.CIRCLE)
pl.drawLine(xb[0], yb[0], xb[1], yb[1])
pl.show() 

