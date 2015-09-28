# testProcAZtecTif.py
#
# J. R. Minter
#
# Process an AZtec.tif image, setting reproducible contrast limits and
# appying a median filter
#
# CCA licence
#  date       who                            comment
# ----------  ---  -----------------------------------------------------
# 2015-09-28  JRM  Initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

def procAZtecImg(imp, loG, hiG, radMF, unPerPx, units=-6):
	"""procAZtecImg(imp, loG, hiG, radMF, unPerPx, units=-6)
	Process an AZTec TIF image
	Inputs:
	imp     - the image plus
	loG     - the gray level to set as black
	hiG     - the gray level to set as white
	radMF   - the radius for a median filter
	unPerPx - the size of a pixel in units
	units   - the power w.r.t. meters. Default = -6
	
	Returns:
	an image plus of a duplicated image
	"""
	name = imp.getShortTitle()
	# make a copy
	wrk = imp.duplicate()
	IJ.run(wrk, "Median...", "radius=%g" % radMF)
	IJ.setMinAndMax(wrk, loG, hiG)	
	jmg.calibImageDirect(wrk, unPerPx, units=-6)
	wrk.setTitle(name)
	return wrk


imp = IJ.getImage()
res = procAZtecImg(imp, 3000,12000, 1.0, 0.011328, units=-6)
res.show()
	
	