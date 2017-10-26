from ij import IJ
import jmFijiGen as jmg

bCvtToRgb = True

imp = IJ.getImage()
jmg.setFullGrayDisplayRange(imp, bCvtToRgb=True, bVerbose=True)

