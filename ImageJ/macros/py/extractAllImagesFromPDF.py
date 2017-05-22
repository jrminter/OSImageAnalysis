from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
ImageJ - J. R. Minter - 2016-10-12

CCA licence

  date      who  Ver     Comment
----------  ---  ------  -----------------------------------------------
2017-05-21  JRM  1.0.00  Extract images from a PDF File and store as
                         PNG images
"""


import os
import glob
import time

from ij import IJ, Prefs
from ij import ImagePlus
from ij.io import FileSaver, DirectoryChooser
import jmFijiGen as jmg

bVerbose = False
inFold = "/Users/jrminter/Documents/lit/microanalysis/eds/"
ouFold = "/Users/jrminter/Desktop/tmp/"
fName  = "Ritchie2011d"



def autoExtractPDF(folderPathIn, folderPathOut, fileName):
    """autoExtractPDF(folderPathIn, folderPathOut, fileName)

    A wrapper function to extract all images from a PDF file
    and store them as PDF files in an output folder.

    Parameters
    ----------
    folderNameIn : string
        The path to the input folder (with a path terminator character)
    folderNameOut : string
        The path to the output folder (with a path terminator character)
    fileName : string
        base name of the PDF file (foo)

    Example:
    inFold = "/Users/myId/lit/eds/"
    ouFold = "/User"/myId/png/
    fName = "author.pdf"
    autoExtractPDF(inFold, ouFold, fName)

    """
    IJ.run("Close All")
    fIn = folderPathIn + fileName + ".pdf"
    strTwo = "choose=%s" % (fIn)
    print(strTwo)
    IJ.run("Extract Images From PDF...", strTwo )
    while (IJ.getImage() != None):
        imp = IJ.getImage()
        basName = imp.getShortTitle()
        print(basName)
        fiOut = folderPathOut + basName + ".png"
        print(fiOut)
        IJ.saveAs(imp,"PNG",fiOut)
        imp.changes = False
        imp.close()



autoExtractPDF(inFold, ouFold, fName)



    