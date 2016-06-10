# makeTifFromDm3.py
#
# J. R. Minter
#
# Process a folder of .DM3 files create 16 bit TIF files for ImageJ
# expects a subfolder "dm3" in a sample folder and puts tifs in
# "tif" subfolder
#
# CCA licence
#  date       who  comment
# ----------  ---  -----------------------------------------------------
# 2016-06/09 JRM  initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
import glob
import time

from ij import IJ
from ij import ImagePlus
import jmFijiGen as jmg

tic = time.time()

imgRt  = os.environ['IMG_ROOT']
relPrj = "/QM16-Cerion-02A-Parsiegla" # "/QM16-01-02A-Nair"
labId  = "qm-04832"
smpId  = "AGFIN15"

sDm3Path = imgRt + relPrj + "/" + labId + "-" + smpId + "/dm3/"
sTifPath = imgRt + relPrj + "/" + labId + "-" + smpId + "/tif/"
jmg.ensureDir(sTifPath)

query = sDm3Path + "*.dm3"
lFiles = glob.glob(query)
print(len(lFiles))
i = 0
for fi in lFiles:
	i += 1
	orig = ImagePlus(fi)
	orig.show()
	strName = os.path.basename(fi)
	strName = strName.split('.')[0]
	outPth = sTifPath + strName + ".tif"
	IJ.saveAs(orig, "TIF", outPth)
	time.sleep(1)
	orig.close()

print("done")
