# WeaverStackExample_.py
# A demo script to show the use of the Weaver for inline java code
#
# adapted from:
# http://fiji.sc/Jython_Scripting#Inline_java_code_inside_jython:_the_Weaver
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-25  JRM 0.1.00  Initial prototype with all the imports
from fiji.scripting import Weaver
from ij import IJ
from ij import ImagePlus
from ij import ImageStack
 
# The currently open image, an 8-bit stack
imp = IJ.openImage("http://imagej.net/images/bat-cochlea-volume.zip")
 
slices = [None, None]
 
w = Weaver.inline(
    """
    byte[] pix1 = (byte[]) slices.get(0);
    byte[] pix2 = (byte[]) slices.get(1);
 
    byte[] xor = new byte[pix1.length];
    for (int i=0; i<pix1.length; i++) {
        xor[i] = (byte)(pix1[i] ^ pix2[i]);
    }
    return xor;
    """,
    {"slices" : slices})
 
stack = imp.getStack()
stackXOR = ImageStack(stack.width, stack.height)
 
for i in range(2, imp.getNSlices()+1):
  # Put the pixel arrays into the pre-made list
  slices[0] = stack.getPixels(i-1)
  slices[1] = stack.getPixels(i)
  # Invoke native code
  stackXOR.addSlice( str(i-1), w.call() )
 
ImagePlus("XORed stack", stackXOR).show()
