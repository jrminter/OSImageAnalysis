# test-db

import os
import shutil
import gov.nist.microanalysis.dtsa2 as dt2
import dtsa2.dbTools as dbt

git = os.environ['GIT_HOME']
edsDir = os.environ['EDS_ROOT']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros"
os.chdir(wd)
pyrDir = wd + "/test-db Results/"



ses = dt2.DTSA2.getSession()

# print(dir(ses))



stds = ses.standards

print(stds)
print(type(stds))
print((stds.lastKey(), stds.lastEntry()))

s = dbt.standardExists(material("Al2O3"))



# clean up cruft
shutil.rmtree(pyrDir)
print("Done!")
