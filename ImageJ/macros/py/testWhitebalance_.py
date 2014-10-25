# testWhitebalance_.py
# White balance an RGB image
# adapkted to python from macro by Vytas Bindokas; Oct 2006, Univ. of Chicago
#
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-25  JRM 0.1.00  Initial prototype to use whiteBalance in jmFijiGen.py
from ij import WindowManager
import jmFijiGen as jmg

test = WindowManager.getCurrentImage()
jmg.whiteBalance(test)