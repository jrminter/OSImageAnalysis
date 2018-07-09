"""
getPrefsDirImageJ.py

ImageJ Jython - J. R. Minter - 2018-07-09

Modifications
 
   Date     Who   Ver                      What
----------  ---  ------  ---------------------------------------------
2018-07-09  JRM  0.1.00  First implementation


"""
from ij import Prefs

st = Prefs.getPrefsDir()
print(st)
