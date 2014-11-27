# summaryTableFun.py
#
# ImageJ Jython - J. R. Minter - 2014-11-27
# Adapted from an idea by Tiago Ferreira tiago.ferreira@mail.mcgill.ca
# on the ImageJ mailing list.
# http://imagej.1557.x6.nabble.com/Data-from-summary-window-td5010658.html
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-27  JRM 1.1.00  Get result from summary table

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')



from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.text import TextWindow

bClose = True

IJ.run("Blobs (25K)")
imp = IJ.getImage()
IJ.setAutoThreshold(imp, "Default")
IJ.run(imp, "Convert to Mask", "")
IJ.run(imp, "Set Measurements...", "area center redirect=None decimal=3")
IJ.run(imp, "Analyze Particles...", "display exclude clear include summarize")
tw = WindowManager.getFrame("Summary")
if tw != None:
    st = tw.getTextPanel().getResultsTable()
    IJ.log("1st row of Summary:\n"+ st.getRowAsString(0))
    v = st.getCounter()
    w = st.getLastColumn()
    s = st.size()
    z = st.getValueAsDouble(w, 0)
    af = float(z)
    af /= 100.
    print("Area Fraction: %.3f" % af)
    
else:
    IJ.log("Summary window not found")

if bClose:
  tw.close()
  imp.changes = False
  imp.close()
  tw = WindowManager.getWindow("Results")
  tw.dispose()