from ij import IJ
import jmFijiGen as jmg



def useSingleLUT(imp, bVerbose=False):
	"""useSingleLUT(imp)
	Check an ImagePlus for a single LUT and activate if found

	Input
	-----
	imp : ImagePlus
		The ImagePlus to be queried for a LUT and have the LUT activated

	bVerbose : A boolean flag (False)
		A flag for verbose messages

	Returns
	-------
		None

	"""
	if bVerbose:
		minV = imp.getDisplayRangeMin()
		maxV = imp.getDisplayRangeMax()
		sMsg = "Current display range: %g - %g" % (minV, maxV)
		print(sMsg)

	luts = imp.getLuts()
	lLUTS = len(luts)
	if (lLUTS == 1):
		if bVerbose:
			print(luts[0])
		imp.setLut(luts[0])
		imp.updateAndRepaintWindow()
	else:
		if bVerbose:
			if(lLUTS > 1):
				sMsg = "Found %g LUTs %s" % (lLUTS, luts)
				print(sMsg)
			else:
				print("No LUTs found")

imp = IJ.getImage()
jmg.useSingleLUT(imp, bVerbose=True)


