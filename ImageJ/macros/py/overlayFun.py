# overlayFun.py
# ImageJ Jython - J. R. Minter - 2014-11-25
# originally from
# http://svn.ehas.org/viewvc.cgi/telemicroscopio/imagej/IJ/ImageJ/plugins/Examples/-Scripts/Create_Overlay.js?revision=28&view=markup&sortby=author&pathrev=28

#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-11-25  JRM 1.1.00  Jython version of Create_Overlay.js

from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ, ImagePlus, WindowManager
from ij.gui import Roi, TextRoi, Overlay, OvalRoi, Line, PolygonRoi
from java.awt import Color, Font

imp = IJ.openImage("http://imagej.nih.gov/ij/images/blobs.gif")

# create an overlay
ol = Overlay()
fnt = Font("SanSerif", Font.BOLD, 28)
roi = TextRoi(10, 5, "This is an overlay", fnt)
roi.setStrokeColor(Color.yellow)
roi.setFillColor(Color(0,0,0,0.5))
ol.add(roi)

roi = Roi(30,70,200,150)
roi.setStrokeColor(Color.blue)
roi.setFillColor(Color(0,0,1,0.3))
ol.add(roi)

roi = OvalRoi(60,60,140,140)
roi.setStrokeColor(Color.green)
roi.setStrokeWidth(15)
ol.add(roi)

roi = Line(30,70,230,230)
roi.setStrokeColor(Color.red)
roi.setStrokeWidth(18)
ol.add(roi)


x = [18,131,148,242]
y = [167,104,232,172];
# roi = PolygonRoi["(int[],int[],int,int)"](x, y, x.length, Roi.POLYLINE);
roi = PolygonRoi(x, y, len(x), Roi.POLYLINE);
roi.fitSpline();
roi.setStrokeColor(Color.blue);
roi.setStrokeWidth(12);
ol.add(roi)
# img.setRoi(roi);

imp.setOverlay(ol)
imp.show()

# we can flatten the image to burn it in if we need to
IJ.run(imp, "Select None", "")
IJ.run(imp, "Flatten", "")

