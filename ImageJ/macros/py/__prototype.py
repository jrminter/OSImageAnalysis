from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')

from ij import IJ

mu = IJ.micronSymbol
scaUni	= mu + "m"

imp = IJ.getImage()
if imp != None:
	cal = imp.getCalibration()
	u = cal.getUnit()
	pw = cal.pixelWidth
	if u == scaUni:
		print("it is")
		print("%.4f" % pw)
	else:
		strU = u.decode()
		strMic = "micron"
		if strU == strMic:
			cal.setUnit(scaUni)
			imp.setCalibration(cal)
			imp.updateAndRepaintWindow()

		else:
			print(strU)
			print(pw)
			
		print("done")
			
			