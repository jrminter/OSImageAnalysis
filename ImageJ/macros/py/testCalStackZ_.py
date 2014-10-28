from ij import IJ
import jmFijiGen as jmg

sx = 0.147
sz = 5.0/21.
sy = sx

theImp = IJ.getImage()
theImp = jmg.calStackZ(theImp, sx, sy, sz, bVerbose=True)
