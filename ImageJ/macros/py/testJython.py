from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')



from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.text import TextWindow

print(dir(IJ))
print(IJ.micronSymbol)
print(IJ.isJava16())
print(IJ.isMacOSX())
