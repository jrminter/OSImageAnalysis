# computeImageDifference.py
#
# A reproducible example showing the problem with JPEG images
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-03-25  JRM 0.1.00  initial prototype

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
from ij import IJ, ImagePlus
from ij.process import FloatProcessor
from ij.plugin import LutLoader
import os

def computeImageDifference(imp1, imp2):
	"""computeImageDifference(imp1, imp2)
	
	Compute the difference between two images

	Parameters
    ----------
	imp1: ImagePlus
        First input image, assumed to be grayscale
    imp2: ImagePlus
        Second input image, assumed to be grayscale

    Returns
	-------
    delta: ImagePlus
    	The difference image as a float
	"""
	ip1 = imp1.getProcessor().convertToFloat() # as a copy
	ip2 = imp2.getProcessor().convertToFloat()
	pix1 = ip1.getPixels()
	pix2 = ip2.getPixels()
	minV = 100000.
	maxV = -100000.
	for i in xrange(len(pix1)):
		dif = abs(pix1[i] - pix2[i])
		# dif = pix1[i] - pix2[i]
		if dif < minV:
			minV =  dif
		if dif > maxV:
			maxV = dif
		pix1[i] = dif
	factor = 1.0/(maxV - minV)
	for i in xrange(len(pix1)):
		pix1[i] = factor*(pix1[i] - minV)
	

	ip3 = FloatProcessor(ip1.width, ip1.height, pix1, None)  
	delta = ImagePlus("Difference", ip3) 
	return delta 

# start clean
IJ.run("Close All","")


gitDir = os.environ['GIT_HOME']
relImg = '/OSImageAnalysis/images/'
imgDir = gitDir+relImg

imgFile = 'mandrill-gray'
# imgFile = 'boats'
lutFile = 'Viridis'

cm = LutLoader.open(imgDir + lutFile + '.lut')

print(imgDir)

ori = IJ.openImage(imgDir + imgFile + '.png')
ori.setTitle("original")
ori.show()

jpg = IJ.openImage(imgDir + imgFile + '.jpg')
jpg.setTitle("jpeg")
jpg.show()

delta = computeImageDifference(ori, jpg)
ip = delta.getProcessor()
pix = ip.getPixels()
width = delta.getWidth()
height = delta.getHeight()
delta = ImagePlus("Difference", FloatProcessor(width, height, pix, cm))
delta.show()







