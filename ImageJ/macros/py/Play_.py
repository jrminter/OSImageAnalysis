from ij import IJ
from ij import ImagePlus
from ij import WindowManager
import doctest
from java.util import Random
imp = IJ.createImage("A Random Image", "8-bit", 512, 512, 1)
Random().nextBytes(imp.getProcessor().getPixels())
# imp.show()
print(dir(doctest))
# doctest.inspect(IJ)