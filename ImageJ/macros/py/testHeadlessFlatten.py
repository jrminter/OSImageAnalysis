# testHeadlessFlatten.py
import os
from ij import IJ
import jmFijiGen as jmg

imgDir = os.environ['IMG_ROOT']
edsDir = os.environ['EDS_ROOT']
relDir = "/Oxford/QM14-nn-nnA-Client/reports/qm-nnnnn-sampleID/qm-nnnnn-sampleID-nnkV-map1/work"
inDir  = edsDir + relDir

pthRoi = inDir + "/ROI.png"
pthCuL = inDir + "/Cu-L.png"

impRoi = IJ.openImage(pthRoi)
impCuL = IJ.openImage(pthCuL)

# headlessFlatten is built into jmg.makeFlattenedTransparentOverlay
impTol = jmg.makeFlattenedTransparentOverlay(impRoi, impCuL, op=50)
# flat = headlessFlatten(impTol)
impTol.show()

outPth = imgDir + "/tmp/foo-fl.png"
IJ.saveAs(impTol, "PNG", outPth)

# imp.show()
# impRoi.show()


