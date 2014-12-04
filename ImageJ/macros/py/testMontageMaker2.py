# testMontageMaker
from ij import IJ, WindowManager, ImageStack, ImagePlus
from ij.io import FileInfo
from ij.plugin import MontageMaker
import jmFijiGen as jmg

IJ.run("Lena (68K)")
lena = IJ.getImage()

lI = [lena, lena, lena]

stack = jmg.makeStackFromListRGB(lI)
mont = MontageMaker()
# starts with a stack (stack) and returns an imp to the montage
# makeMontage2(ImagePlus imp, int columns, int rows, double scale, int first, int last, int inc, int borderWidth, boolean labels) 
imp = mont.makeMontage2(stack, 3, 1, 1.0, 1, 3, 1, 0, False)
imp.show()
