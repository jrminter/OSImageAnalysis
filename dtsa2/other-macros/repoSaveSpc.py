# minimal repo example
# Answer for walter on Probe forum

import dtsa2.mcSimulate3 as mc3
import gov.nist.microanalysis.EPQTools as ept
import java.io as jio
import os
import glob
import shutil

e0       =   20.
nTraj    = 1000
dose     =   60.
addNoise = True
outDir   = "C:/Temp/"

ag = material('Ag', 10.49)

spc = mc3.simulate(ag, d1, e0, dose, addNoise, nTraj, sf=True, bf=True,
                   xtraParams={})

sName = "Bulk-Ag-%g-kV-%g-Traj" % (e0, nTraj)
spc.rename(sName)
spc.display()



fos = jio.FileOutputStream("%s/%s.msa" % (outDir, sName))
ept.WriteSpectrumAsEMSA1_0.write(spc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)

