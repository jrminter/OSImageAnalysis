from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ
import jmFijiGen as jmg

def cropImage(imp, x0, y0, w, h, bTest=False):
	"""cropImage(imp, x0, y0, w, h, bTest=False)
	
	Crop an image from a duplicate and return the ImagePlus of the cropped image
	
	Parameters
	----------
	imp: ImagePlus
		The image to be cropped
	x0: number
		The x coordinate to begin drawing the crop rectangle
	y0: number
		The x coordinate to begin drawing the crop rectangle
	w: number
		The width in pixels for the box
	h: number
		The height in pixels for the box		
	bTest: Boolean (False)
		If True, just draw the rectangle

	Returns
	-------
	ret: ImagePlus
		The cropped image
	"""
	IJ.run("Colors...", "foreground=black background=black selection=green")
	IJ.makeRectangle(x0, y0, w, h)
	if(bTest==True):
		return
	else:
		ret = imp.crop()
		return ret




imp = IJ.getImage()

cr = jmg.cropImage(imp, 10, 10, 100, 100)
cr.show()

