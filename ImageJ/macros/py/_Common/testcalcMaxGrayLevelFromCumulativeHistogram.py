from ij import IJ
import jmFijiGen as jmg

imp = IJ.getImage()
thr = jmg.calcMaxGrayLevelFromCumulativeHistogram(imp, 0.99)
print(thr)
    