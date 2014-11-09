# testSignedUnsignedCmci.py
#
# adapted from http://cmci.embl.de/documents/120206pyip_cooking/python_imagej_cookbook#singedunsigned_value_conversions
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-07  JRM 0.1.00  initial test

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ
import struct
 
def s2u8bit(v):
    return struct.unpack("B", struct.pack("b", v))[0]


IJ.run("Blobs (25K)")
  
imp = IJ.getImage()
signedpix = imp.getProcessor().getPixels()
  
pix = map(s2u8bit,signedpix)
  
#check that the conversion worked. 
# this example was made for binary image, to print only values 255  
for j in range(len(pix)):
        curval = pix[j]
        #curval = s2u8bit(curval)
        if curval is 0:
            print '--'
        else:
            print curval