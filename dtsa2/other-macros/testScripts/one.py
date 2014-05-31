# -*- coding: utf-8 -*-
#         1         2         3         4         5         6         7 |
# 23456789012345678901234567890123456789012345678901234567890123456789012
#
# one.py
# jrm 2014-05-30 - Test ruleThemAll
# 

import os
import shutil
import dtsa2.jmGen as jmg
import time

git = os.environ['GIT_HOME']
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/one Results"
start = time.time()
print("running one")
jmg.elapsedTime(start)

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
