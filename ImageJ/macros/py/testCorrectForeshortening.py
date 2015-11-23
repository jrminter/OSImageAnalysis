import math
from ij import IJ, ImagePlus
import jmFijiGen as jmg

imp = IJ.getImage()

# ret = jmg.medianFilter(imp, 1.0)
ret = jmg.correctForeshortening(imp, 38.0)
