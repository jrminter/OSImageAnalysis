from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ
from ij.plugin import Duplicator

imgPath = '/Users/jrminter/dat/images/test/qm-04570-1421DJD-04-C03/1421DJD-04-C03-SegA-01.tif'
imp = IJ.openImage(imgPath)
imp.show()

def removeOutliers(imp, radius, threshold, bright):
  """ Apply a remove outliers filter to a copy
      of the given ImagePlus, and return it. """
  copy = Duplicator().run(imp)
  which = "Bright" if bright else "Dark"
  IJ.run(copy, "Remove Outliers...", "radius=" + str(radius) \
      + " threshold=" + str(threshold) + " which=" + which)
  return copy

imp2 = removeOutliers(imp, 2., 75, True)

imp2.show()

