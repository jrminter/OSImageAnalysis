from ij import IJ
import jmFijiGen as jmg

bCvtToRgb = False
factor = 0.7
mu = IJ.micronSymbol
scaUm = mu + "m"


imp = IJ.getImage()
jmg.setFullGrayDisplayRange(imp, factor=factor, bCvtToRgb=bCvtToRgb, bVerbose=True)

