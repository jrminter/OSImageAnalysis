# measGrayStatsTifDir.py
#
# J. R. Minter
#
# Process a folder of .tif files and measure gray level stats
#
# CCA licence
#  date       who   comment
# ----------  ---	-----------------------------------------------------
# 2015-09-29  JRM   ability to set gray levels


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from org.apache.commons.math3.stat.descriptive import DescriptiveStatistics as DSS
from ij.measure import ResultsTable
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
imgRt = os.environ['IMG_ROOT']
rPrjDir = "QM15-09-02B-Rollins"
ePrjDir = "QM15-09-02B2-Rollins"
labId = "qm-04475"
smpId = "7449-483-14F-UNKE-better"

datDir	 = edsDir + "/Oxford/" + ePrjDir + "/reports/" + labId + "-" + smpId
sTifPath = datDir + "/tif/"
sCsvPath = datDir + "/csv/"

print(sTifPath)

IJ.run("Set Measurements...", "mean modal min redirect=None decimal=3");



query = sTifPath + "*.tif"
print(query)
lFiles = glob.glob(query)
i = 0
for fi in lFiles:
	i += 1
	fi = fi.replace("\\", "/")
	print(fi)
	orig = ImagePlus(fi)
	strName = os.path.basename(fi)
	strName = strName.split('.')[0]
	lStr = strName.split('-')
	ti = orig.getShortTitle()
	orig.setTitle(ti)
	IJ.run(orig, "Measure","")
	time.sleep(1)
	orig.close()

rt = ResultsTable.getResultsTable()
nMeas = rt.getCounter()
minC = rt.getColumnIndex("Min")
maxC = rt.getColumnIndex("Max")
minStats = DSS()
maxStats = DSS()
for i in range(nMeas): 
	minVal = rt.getValueAsDouble(minC, i)
	minStats.addValue(minVal)
	maxVal = rt.getValueAsDouble(maxC, i)
	maxStats.addValue(maxVal)

meanMinVal = minStats.getMean()
meanMaxVal = maxStats.getMean()

strOut = "mean minimum gray = %.2f, mean maximum gray = %.2f" % (meanMinVal, meanMaxVal)

print(strOut)

rt.reset()
# rt.updateResults()

win = rt.getResultsWindow()
win.close()

toc = time.time()

elapsed = toc - tic

print("analyzed %g images" % i)
print("completed in %g sec" % elapsed )

