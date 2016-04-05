# estimateAztecScaleFactorX.py
# A script to write metadata for an AZtec image to an ini file
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2016-04-05  JRM 0.1.00  Initial prototype  - a work in progress

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

def estimateAztecScaleFactorX(mag, scanWidthPx=1024, slope=289251.80, slopeSE=16.54, rDigits=7):
	"""estimateAztecScaleFactorX(mag, scanWidthPx=1024, slope=289251.80, slopeSE=16.54
	
	Estimate the scale factor [microns/px] from a linear fit of the image full width
	as a function of the inverse magnification.

	Parameters
    ----------
    mag: number
        The SEM magnification
    scanWidthPx: number (1024)
    	The full width of the image scan in pixels. The maximum is 4096
    slope: number (289251.80)
    	The slope of the inverse magnification plot. Note the intercept is constrained
    	to zero.
    slopeSE: number (16.54)
    	The standard error of the fit.  
    rDigits: integer (5)
    	Number of digits to round the microns/pix

    Returns
    -------
    sf: list [mean, LCL, UCL]
    	The scale factor in microns per pixel. The first value is the mean.
    	The second and third values are the lower and upper confidence intervals.
	"""
	imFWMu  = slope/mag
	imFWLCL = (slope-slopeSE)/mag
	imFWUCL = (slope+slopeSE)/mag
	sfMu = round(imFWMu/scanWidthPx, rDigits)
	sfLC = round(imFWLCL/scanWidthPx, rDigits)
	sfUC = round(imFWUCL/scanWidthPx, rDigits)
	sf = [sfMu, sfLC, sfUC]
	return sf

out = estimateAztecScaleFactorX(50000.)
print(out)