# testImageDiff.py
#
# J. R. Minter
#
# calculate the difference between two images
#
# CCA licence
#  date       who  Comment
# ----------  ---  -----------------------------------------------------
# 2016-03-24  JRM  inital prototype

def imgDif(imp1, imp2):
	"""
	imgDif(imp1, imp2)

	Compute the difference between images
	"""
	ip1 = imp1.getProcessor()
	ip2 = impq.getProcessor()
	mode = Blitter.SUBTRACT