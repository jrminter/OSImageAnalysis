# -*- coding: utf-8 -*-
#         1         2         3         4         5         6         7  
#123456789012345678901234567890123456789012345678901234567890123456789012
#
# 4_testTabCalibrations.py
# 
# tabulate calibrations for a selected detector
# J. R. Minter 2014-05-30 - initial version. Source in git repository
import os
import shutil
import java.io as jio
import math
import dtsa2.jmGen as jmg

git = os.environ['GIT_HOME']
edsDir = os.environ['EDS_ROOT']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/4_testTabCalibrations Results/"

sDet = "FEI CM20UT EDAX-RTEM"


  
det = findDetector(sDet)
sRpt = wd + '/cm20ut-cal.csv'
jmg.tabulateDetCalibrations(det, sRpt)

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"

