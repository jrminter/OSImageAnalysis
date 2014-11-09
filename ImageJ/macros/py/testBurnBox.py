from ij import IJ
import jmFijiGen as jmg

IJ.run("Blobs (25K)")
lRoi = [50, 50, 128, 128]
raw = IJ.getImage()
jmg.burnBox(raw, lRoi, col="green", wid=4)
