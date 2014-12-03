# testMakeStack.py

from ij import IJ, WindowManager, ImageStack, ImagePlus
from ij.io import FileInfo
import jmFijiGen as jmg
  

IJ.run("Lena (68K)")
lena = IJ.getImage()

lI = [lena, lena, lena]

myStack = jmg.makeStackFromListRGB(lI)

myStack.show()



