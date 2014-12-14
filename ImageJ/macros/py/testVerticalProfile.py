# testVerticalProfile.py
#
# Test a vertical profile from a latex image
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-12-14  JRM 0.1.00  Initial test of a vertical profile from a latex image

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os, csv, time
from ij import IJ
import jmFijiGen as jmg

homDir  = os.environ['HOME']
gitDir  = os.environ['GIT_HOME']
edsDir  = os.environ['EDS_ROOT']
relImg  = "/Oxford/QM14-nn-nnA-Client/reports/qm-nnnnn-sampleID/tif"
imgPath = edsDir + relImg + "/latex.tif"
relPrj  = "/work/proj/QM14-nn-nnA-Client"
proDir  = homDir + relPrj 
proPth  = proDir + "/dat/csv/latexPro.csv"


imp = IJ.openImage(imgPath)
  
# pro = jmg.doCrop(imp, [24,24,32,32])

[x, y] = jmg.vertProfileFromROI(imp, [343, 436, 11, 68], 1.0, bHeadless=True)




# open the file first (if its not there, newly created)
print("writing output")
f = open(proPth, 'wb')
# create csv writer
writer = csv.writer(f)
# write the header
row = ["x", "y"]
writer.writerow(row)
 
# for loop to write each row
for i in range(len(x)):
  row = [x[i], y[i]]
  writer.writerow(row)
 
# close the file. 
f.close()
print("done")

