from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

"""
ImageJ - J. R. Minter - 2016-10-12

CCA licence

  date      who  Ver     Comment
----------  ---  ------  -----------------------------------------------
2017-05-22  JRM  1.0.00  Extract images from a PDF File and store as
                         PNG images
"""


import os
import jmFijiGen as jmg

litDir = os.getenv('LIT_ROOT')
imgDir = os.getenv('IMG_ROOT')

bVerbose = False
inFold = litDir + "/microanalysis/eds/"
ouFold = imgDir + "/extracted/"
fName  = "Ritchie2011d"

print(inFold)
print(ouFold)



# use the lib version...
jmg.autoExtractPDF(inFold, ouFold, fName)



    