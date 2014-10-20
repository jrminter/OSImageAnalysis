# test makeStackFromDir
# from
# http://cmci.embl.de/documents/120206pyip_cooking/python_imagej_cookbook#pluginextended_depth_of_field_easy_mode
#  Modifications
#   Date      Who  Ver                       What
# ----------  --- ------  -------------------------------------------------
# 2014-10-20  JRM 0.1.00  copied from source with minor adaptations
#                         TO DO: figure out expert mode from exemplar
from org.python.core import codecs
codecs.setDefaultEncoding('utf-8')
import jmFijiGen as jmg

inpDir = 'D:/Data/images/efi-test/50X-2/'


myImp = jmg.makeStackFromDir(inpDir, inExt='.tif', bDebug=False)


