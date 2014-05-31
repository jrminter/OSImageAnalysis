# -*- coding: utf-8 -*-
#         1         2         3         4         5         6         7 |
# 23456789012345678901234567890123456789012345678901234567890123456789012
#
# ruleThemAll.py
#
# A wrapper script to run several other time-consuming scripts that will
# record their run times...
#
# jrm 2014-05-31 - Tests calling scripts that call to elapsedTime in
#                  jmGen
# 

import os
import shutil
import time

git = os.environ['GIT_HOME']
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/ruleThemAll Results/"
sOne = wd + "/one.py"
sTwo = wd + "/two.py"

run(sOne)
run(sTwo)


# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
