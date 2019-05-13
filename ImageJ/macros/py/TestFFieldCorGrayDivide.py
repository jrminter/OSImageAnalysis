# testFlatFieldDivide.py
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2019-05-12  JRM 0.1.00  Test function in jmFijiGen.py


from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

import os

from ij import IJ
from ij.plugin import ImageCalculator
import jmFijiGen as jmg


def FlatFieldCorrectGrayDivide(impImg, impFF):
    """
    FlatFieldCorrectGrayDivide(impImg, impFF)

    Do a flat-field (shading) correction for an gray scale image

    Parameters
    ----------
    impImg: ImagePlus
        The image plus for a gray scale image to correct for shading
    impFF: ImagePlus
        A no-sample gray scale image (gain) 

    Returns
    -------
    impSc: ImagePlus
        The corrected image

    TO DO: error checking

    Example
    -------
    import os
    from ij import IJ
    import jmFijiGen as jmg

    """
    name = impImg.getShortTitle()
    ic = ImageCalculator()
    imp = ic.run("Divide create 32-bit", impImg, impFF)
    imp.setTitle(name + "_ffc")
    imp.show()
    return imp

print(jmg.getVersion())
print(os.getenv('HOME'))
imgPath = os.getenv('IMG_ROOT') + "/key-test/ff-test/IAM-1-Stage-Micrometer/IAM-1-Stage-Micrometer.tif"
print(imgPath)
ffPath = os.getenv('IMG_ROOT') + "/key-test/ff-test/IAM-1-Stage-Micrometer/Blank-Int-10.tif"
print(ffPath)

IJ.run("Close All")
impImg = IJ.openImage(imgPath)
impImg.show()

impFF = IJ.openImage(ffPath)
impFF.show()

impCor = jmg.FlatFieldCorrectGrayDivide(impImg, impFF)
impCor.show()
