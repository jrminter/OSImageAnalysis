# testHeadlessFlatten.py
import os
from ij import IJ, ImagePlus
from ij.gui import ImageRoi
import jmFijiGen as jmg

def headlessFlatten(imp):
  flags = imp.isComposite()
  if flags==False:
    IJ.setupDialog(imp, 0)
  ret = imp.flatten()
  ret.setTitle(imp.getShortTitle())
  return ret
  
  
  

op = 50.

homDir = os.environ['HOME']
edsDir = os.environ['EDS_ROOT']
relDir = "/Oxford/QM14-nn-nnA-Client/reports/qm-nnnnn-sampleID/qm-nnnnn-sampleID-nnkV-map1/work"
imgDir = edsDir + relDir

pthRoi = imgDir + "/ROI.png"
pthCuL = imgDir + "/Ag-L.png"

impRoi = IJ.openImage(pthRoi)
impCuL = IJ.openImage(pthCuL)

impTol = jmg.makeFlattenedTransparentOverlay(impRoi, impCuL, op=30)

impTol.show()



# flat = headlessFlatten(imp)

outPth = homDir + "/Desktop/foo-fl.png"

# IJ.saveAs(flat, "PNG", outPth)

# imp.show()
# impRoi.show()


