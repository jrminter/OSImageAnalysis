# -*- coding: utf-8 -*-

"""
         1         2         3         4         5         6         7 |
123456789012345678901234567890123456789012345678901234567890123456789012

sim-ir-on-ag-on-sio2.py

Modifications

Who     When                        Comments
---  ----------  -------------------------------------------------------

jrm  2018-07-16  Use mc3 to simulate Ir/Ag//SiO2


Background

> From: http://probesoftware.com/smf/index.php?topic=1104.0
> 
> We were having trouble identifying features on a sample, including
> various thin film coatings, so as a last resort we ran EDS mapping
> to help us get oriented, but suspecting that there would be very
> little signal from the thin films. We assigned some low energy peaks
> to Ir, even though some higher energy peaks were absent, as we knew
> Ir was present as a thin film and no other element matched the energy
> more closely. We were pleasantly surprised that Ir was accurately
> mapped (see image). Comparing the peaks we measured to the peaks
> predicted by Inca (attached), the L peaks up around 10 keV are
> barely present, and the M peaks down around 2 keV are in the wrong
> proportions relative to each other. Analysis performed at 12 kV.
>
> The thin iridium film (light area) in the map image, has a thin silver
> underlayer and both are on a silica substrate. Thicknesses to be
> determined, probably around 500 nm for the Ir, and much thinner for
> the silver.
> 
> We suspect that the 12 kV beam passed right through the Ir/Ag
> generating very little signal, and that 1.7 keV X-rays from the Si
> beneath have excited a fluorescence in the Ir giving a strong Ir
> peak at around 1.55 keV. All other Ir peaks are from a weak
> interaction with the electron beam. Does this sound plausible? If not,
> we'd love to hear what you think is going on. I guess it might be
> useful to run at 3 kV and see if the relative size of the M peaks
> changes. Angling the sample might also have an effect.
> 
> Disclaimer: our EDS system requires calibration as discussed elsewhere
> on the forum, but can be persuaded to produce spectra and maps.
> 
> Thanks for reading, we look forward to any comments.

Times on my MacBook Pro (Late 2013)

0:09:38.7 for 10000 traj for 100 nm Ir  50 nm Ag on SiO2 at 30kV
0:12:42.6 for 10000 traj for 200 nm Ir 100 nm Ag on SiO2 at 30kV
0:17:25.0 for 10000 traj for 400 nm Ir 200 nm Ag on SiO2 at 30kV
0:17:19.6 for 10000 traj for 500 nm Ir 200 nm Ag on SiO2 at 30kV

"""

import sys
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3, FluorescenceXRayGeneration3, XRayTransport3", None)
import gov.nist.microanalysis.EPQLibrary as epq
import gov.nist.microanalysis.EPQLibrary.Detector as epd
import gov.nist.microanalysis.NISTMonte as nm
import gov.nist.microanalysis.NISTMonte.Gen3 as nm3
import gov.nist.microanalysis.EPQTools as et
import dtsa2.mcSimulate3 as mc3
import java.util as jutil
import java.io as jio
import java.nio.charset as cs
import os
import glob
import shutil
import time

def ensureDir(d):
    """ensureDir(d)
    Check if the directory, d, exists, and if not create it."""
    if not os.path.exists(d):
        os.makedirs(d)

print("Date & time started: " + time.strftime("%c"))

tNmIr   =   250.0  # nm of Ir top layer
tNmAg   =   150.0  # nm of Ag 2nd layer
nTraj   = 10000    # num Traj to run per pt 10000 for a long run
charF   =  True    # include characteristic fluorescence
bremF   =  True    # include continuum fluorescence 
pc      =     2.5  # nA
lt      =   100.0  # sec
e0      =    30.0  # keV
imgSize =   512    # pixel size for images
imgSzUm =     5.0  # image size in microns
vmrlEl  =    40    # number of el for VMRL

dose    = pc * lt  # nA sec
title   = "%gnm-Ir-on-%g-nm-Ag-on-SiO2-%gkV" % (tNmIr, tNmAg, e0)

gitDir = os.environ['GIT_HOME']
relPrj = "/OSImageAnalysis/penepma"
pyDir  = gitDir + relPrj + "/dtsa/py"

datDir = gitDir + relPrj + "/trilayer-Ir-250nm-Ag-150nm-Silica"
csvDir = datDir + "/csv"
simDir = datDir + "/sim"


ensureDir(datDir)
ensureDir(csvDir)
ensureDir(simDir)

os.chdir(pyDir)
pyrDir = "./sim-ir-on-ag-on-sio2 Results"

# can use
# det  = findDetector("Si(Li)")
det  = findDetector("Oxford p4 05eV 4K")
print(det)

if 'defaultXtraParams' not in globals():
   defaultXtraParams = {}
if 'defaultBremFluor' not in globals():
   defaultBremFluor = False
if 'defaultCharFluor' not in globals():
   defaultCharFluor = False
if 'defaultNumTraj' not in globals():
   defaultNumTraj = 1000
if 'defaultDose' not in globals():
   defaultDose = 120.0

# start clean
DataManager.clearSpectrumList()


sio2 = material("SiO2", density= 2.65)
ir   = material("Ir",   density=22.56)
ag   = material("Ag",   density=11.9)

# define the desired transitions
xrts=mc3.suggestTransitions("SiOIrAg")
# print(xrts)
# set up the extra parameters
xtraParams={}
xtraParams.update(mc3.configureXRayAccumulators(xrts, charAccum=charF, charFluorAccum=charF, bremFluorAccum=bremF))
# note that the image size on the specimen is in meters...
xtraParams.update(mc3.configureEmissionImages(xrts, imgSzUm*1.0e-6, imgSize))
xtraParams.update(mc3.configurePhiRhoZ(imgSzUm*1.0e-6))
xtraParams.update(mc3.configureTrajectoryImage(imgSzUm*1.0e-6, imgSize))
xtraParams.update(mc3.configureVRML(nElectrons = vmrlEl))
xtraParams.update(mc3.configureOutput(simDir))

print(xtraParams)

layers = [ [ir, tNmIr*1.0e-9],
           [ag, tNmAg*1.0e-9],
           [sio2, 50.0e-6]
         ]

spc = mc3.multiFilm(layers, det, e0, True, nTraj,
                    dose, True, True, xtraParams)

display(spc)

strFi = datDir + "/" + title + ".msa"

spc.save(strFi)






shutil.rmtree(pyrDir)
print("Done!")
print("Date & time finished: " + time.strftime("%c"))

