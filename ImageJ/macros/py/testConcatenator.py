"""
testConcatenator.py

  Modifications
   Date      Who  Ver                       What
----------  --- ------  -------------------------------------------------
2018-03-12  JRM 0.1.00  Concatenate images into a stack. Based on an 
                        example from Wayne Rasband postecd to the IJ
                        mailing list.
"""

from ij import IJ
from ij.plugin import Concatenator

IJ.run("Close All")

IJ.run("Boats (356K)")
i1 = IJ.getImage()

IJ.run("Bridge (174K)")
i2 = IJ.getImage()

i3 = Concatenator.run(i1, i2)
i3.show()


