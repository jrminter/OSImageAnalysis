/**
* Symbol Example
* Wayne Rasband 
* importClass added by JRM
**/
importClass(Packages.ij.IJ);
// importClass(Packages.ij.Overlay);
// importClass(Packages.ij.gui.ProfilePlot);
// importClass(Packages.ij.TextRoi);
importClass(java.awt.Font);

text = "Delta (\u0394), micron (\u00B5) and angstrom (\u00C5)";
img = IJ.openImage("http://wsr.imagej.net/images/hela-cells.zip");
font = new Font("SansSerif", Font.PLAIN, 24);
// roi = new TextRoi(20, 20, text, font);
// roi.setStrokeColor(Color.yellow);
// overlay = new Overlay(roi);
// img.setOverlay(overlay);
// img.show();
