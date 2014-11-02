from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os, csv, time
from ij import IJ
import jmFijiGen as jmg

gitDir = os.environ['GIT_HOME']
relImg = "/OSImageAnalysis/images"
imgPath = gitDir + relImg + "/latex.tif"

pause = 0.1

imp = IJ.openImage(imgPath)

if (pause > 1.99):
  imp.show()
  
# pro = jmg.doCrop(imp, [24,24,32,32])
# pro.show()

[x, y] = jmg.vertProfileFromROI(imp, [343, 436, 11, 68], 1.0, pause=pause)

# print(x,y)

proDir = gitDir + relImg 
proPth = proDir + "/latexPro.csv"

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



