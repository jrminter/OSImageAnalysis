"""
Latex watershed example

   Date          Who      What
----------  -----------  ---------------------------------------------
2019-05-15  John Minter  Initial test. Inspired by this page:
                         https://imagej.net/Classic_Watershed

"""
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import os
from ij import IJ
from ij.plugin.filter import Analyzer

# parameters

imgDir = os.environ['IMG_ROOT']
print(imgDir)

# Image Path
strImgDir = imgDir + "/key-test/pol4455/"
strImgNam = "POL-4455-16bit-Img01-bks.dm3"
strCsvNam = "POL-4455-16bit-Img01-bks.csv"
strImgPath = strImgDir + strImgNam
strCsvPath = strImgDir + strCsvNam
print(strImgPath)

# median filter radius
rad = 2
strRadius = "radius=%i" % (rad)


# max intensity for dark latex particles 
maxIntensityLatex = 134
# size for the Gaussian Blur
gbSigma = 5
# saturated fraction
satFrac = 0.35
strFrac = "saturated=%f" % (satFrac)

# base name for the processed blurred latex image
strName = "latex-blur"

# set the string for the Gaussian Blur
gbStr2 = "sigma=%i" % (gbSigma)

# set the strings for processing the blurred latex image
strTitle = strName + ".dm3"
strWS2 = "input=%s mask=None use min=0 max=%i" % (strName, maxIntensityLatex)

# start clean...
IJ.run("Close All")

IJ.open(strImgPath);
IJ.run("Median...", strRadius);
IJ.run("Enhance Contrast", strFrac)
Analyzer.setOption("ScaleConversions", True)
IJ.run("8-bit");
IJ.run("Gaussian Blur...", gbStr2)
imp = IJ.getImage()
imp.setTitle(strTitle)
IJ.run("Classic Watershed", strWS2)
# prepare for analyze particles
IJ.run("8-bit")
imp = IJ.getImage()
IJ.setThreshold(imp, 1, 255)
IJ.run("Convert to Mask")

# size in nm now
IJ.run("Analyze Particles...", "size=2000.0-20000.0 circularity=0.6-1.00 show=Outlines display exclude summarize add");
IJ.saveAs("Results", strCsvPath);
# IJ.run("Analyze Particles...", "size=0.002-0.02 show=Outlines display exclude summarize add");
# apply LUT to facilitate result visualization
# IJ.run("3-3-2 RGB")