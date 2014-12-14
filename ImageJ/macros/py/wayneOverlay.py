from ij import IJ
from ij.gui import ImageRoi
  
img = IJ.openImage("http://imagej.nih.gov/ij/images/leaf.jpg")
img2 = IJ.openImage("http://imagej.nih.gov/ij/images/clown.jpg")
ip = img2.getProcessor()
# ip = ip.convertToByte(False)
imageRoi = ImageRoi(100, 100, ip)
imageRoi.setOpacity(0.5)
img.setRoi(imageRoi)
img.show()