# testDSS.py

from ij import IJ, WindowManager
from ij.process import ImageProcessor
from ij.measure import Calibration, ResultsTable
from org.apache.commons.math3.stat.descriptive import DescriptiveStatistics

# set to True if you want to close intermendiate windows
bClose = False
IJ.run("Blobs (25K)")
imp = IJ.getImage()
imp.show()
IJ.setAutoThreshold(imp,"Otsu")
IJ.run(imp, "Convert to Mask","")
IJ.run(imp, "Set Measurements...", "area add redirect=None decimal=3")
IJ.run(imp, "Analyze Particles...", "display exclude clear")
rt = ResultsTable.getResultsTable()
areas = rt.getColumnAsDoubles(rt.getColumnIndex("Area"))
if bClose:
  IJ.run("Clear Results")
  w=WindowManager.getWindow("Results")
  w.close()

stats = DescriptiveStatistics()
for area in areas:
  stats.addValue(area)

mu     = stats.getMean()
sd     = stats.getStandardDeviation()
median = stats.getPercentile(50)

print(mu, sd, median)

