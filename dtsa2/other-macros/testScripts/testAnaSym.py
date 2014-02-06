# -*- coding: utf-8 -*-
#
# testAnaSym.py
#
# Test an analytical spectrum simulation
# 2014-02-06 J. R. Minter

import os
import shutil


ghDir = os.environ['GIT_HOME']
rlDir = "/OSImageAnalysis/dtsa2/other-macros/testScripts/"
wkDir = ghDir + rlDir
os.chdir(wkDir)
pyrDir="./testAnaSym Results"

e0 = 25      # accelerating voltage kV
ia = 0       # incident angle deg
pc = 10.0    # probe current nA*sec
mat = material("Cu", density=8.96)
sDet = "FEI FIB620 EDAX-RTEM"
det = findDetector(sDet)


spec = simulate(mat, det, keV=e0, dose=pc, withPoisson=True)
display(spec)


# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"