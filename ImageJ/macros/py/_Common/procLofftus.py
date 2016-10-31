"""
procLofftus.py

Set the display limits for the current image plus

Modifications

   Date      Who  Ver                       What
----------  --- ------  ------------------------------------------------
2016-10-31  JRM 0.1.00  Initial prototype

"""


from ij import IJ

bT = True

lo = 200.
hi = 3000.

 
imp = IJ.getImage()
iWid = imp.getWidth() 

ip = imp.getProcessor()
imp.setDisplayRange(lo, hi)
imp.updateAndRepaintWindow()
if bT:
	IJ.run(imp, "RGB Color", "")
	IJ.run("Add Scale Bar", "width=1 height=6 font=18 color=White location=[Lower Right] bold");
	
imp.updateAndRepaintWindow()
