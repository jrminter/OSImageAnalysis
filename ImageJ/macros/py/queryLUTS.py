# queryLUTS.py

from ij import IJ

imp = IJ.getImage()
luts = imp.getLuts()
lLUTS = len(luts)
if (lLUTS > 0):
	print(luts)

