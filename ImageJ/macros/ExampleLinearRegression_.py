from array import array
from ij import IJ
from ij.measure.CurveFitter import *
# Example from 
# http://rsbweb.nih.gov/ij/macros/examples/CurveFittingDemo.txt
# x = array('d', [0, 1, 2, 3, 4, 5])
# y = array('d', [0, 0.9, 4.5, 8, 18, 24])
#
# make one where I know approximate coefficients
x = array('d', [0, 1,   2,   3,    4,    5])
y = array('d', [0, 1.1, 1.9, 2.95, 4.02, 4.99])
cf=CurveFitter(x,y)
cf.doFit(STRAIGHT_LINE)
res=cf.getParams()
# N.B. cf.getParams() returns
# [ intercept, slope, sum of square residuals]
b = res[0]
m = res[1]
p3 = res[2]
print "Linear fit example: b=" + IJ.d2s(b,6) + ", m =" + IJ.d2s(m, 6) + ", par3=" + IJ.d2s(p3, 6) 
print cf.getResultString()


