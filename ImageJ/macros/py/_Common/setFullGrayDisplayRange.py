from ij import IJ
import jmFijiGen as jmg

bCvtToRgb = True

imp = IJ.getImage()
bd = imp.getBitDepth()
print(bd)
if(bd==24):
	IJ.run(imp,"16-bit","")
	bd = 16
jmg.setFullGrayDisplay(imp)
if(bd==16):
	if(bCvtToRgb==True):
		IJ.run(imp,"RGB Color","")
