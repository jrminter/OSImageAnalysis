# -*- coding: utf-8 -*-
#
# modPdInCu7kV.py
# jrm 2014-05-03
# 
# Compute a .rpl file for 0.2 um Pd cube in Cu. This version
# corrects a real spectrum for a Lispix file
import gov.nist.microanalysis.EPQLibrary as epq
import gov.nist.microanalysis.EPQLibrary.Detector as epd
import gov.nist.microanalysis.NISTMonte as nm
import gov.nist.microanalysis.EPQTools as et
import java.util as jutil
import java.io as jio
import java.nio.charset as cs
import os
import shutil

def ensureDir(d):
  """ensureDir(d)
  Check if the directory, d, exists, and if not create it."""
  if not os.path.exists(d):
    os.makedirs(d)

edsDir = os.environ['EDS_ROOT']
relDir = "/modelPdOnCu"
wd = edsDir + relDir + "/py"
os.chdir(wd)
pyrDir = wd + "/modPdInCu7kV Results"
datDir = edsDir + relDir + '/dat'
ensureDir(datDir)

nTraj   =  250      # num Traj to run per pt
charF   =   1      # include characteristic fluorescence
bremF   =   1      # include continuum fluorescence 
pdSize  =   0.20   # Pd block size in microns   
radius  =   5.0e-7 # radius in meters
sc      =   1.0e-6 # scale blocks microns to meters
pc      =   2.5    # nA
lt      = 100.0    # sec
e0      =   7.0     # keV

# For now, just simulate a centered 200 nm thick Pd cube in Cu
blocks  = [
#      x        y       z     size 
# [ -0.2500, -0.2500, 0.0100, 0.3000 ],
 [ 0.0000, 0.0000, 0.0200, pdSize ] ] #,
#  [  0.2500, -0.2500, 0.1600, 0.3200 ] ]

baseName = "Pd-%.2f-um-in-Cu-%g-kV" % (pdSize, e0)
datDir = datDir + "/" + baseName
ensureDir(datDir)

# A detector named "Bruker 5" is defined in my DTSA-II preferences (modify!)
# JRM - try  "Lispix 5 eV"  a SDD designed to mimic Oxford XMaxN 80 w 5 eV and 0 offset
# det = findDetector("Lispix 5 eV")
det  = findDetector("Bruker 5 eV")
cw   = det.getChannelWidth()
dp   = det.getProperties()
resn = dp.getNumericProperty(epq.SpectrumProperties.Resolution)

dose = pc * lt # nA sec
# start clean
DataManager.clearSpectrumList()
# Create a Ripple/RAW file (native format for Dave Bright's LISPIX program)
# RippleFile(int width,
#            int height,
#            int depth,
#            java.lang.String dataType,
#            int byteDepth,
#            java.lang.String order,
#            java.lang.String rplFile,
#            java.lang.String rawFile)

rplFil = datDir + "/" + baseName + ".rpl"
rawFil = datDir + "/" + baseName + ".raw"

res=et.RippleFile(64, 64, 2048, et.RippleFile.FLOAT, 4, et.RippleFile.BIG_ENDIAN, rplFil, rawFil)
for x in range(-32,32,1):
  print "Working on row %d" % (x)
  for y in range(-32,32,1):
    if terminated:
      break
    # create an instance of the model
    monte=nm.MonteCarloSS()
    monte.setBeamEnergy(epq.ToSI.keV(e0))
    beam=nm.GaussianBeam(1.0e-9)
    monte.setElectronGun(beam)
    beam.setCenter([0.32*sc*x/32.0,0.32*sc*y/32.0,-0.05])
    # create the sample
    pd = epq.Material(epq.Composition([epq.Element.Pd],[1.0],"Pd"), epq.ToSI.gPerCC(12.023))
    cu = epq.Material(epq.Composition([epq.Element.Cu],[1.0],"Cu"), epq.ToSI.gPerCC(8.96))

    # createBlock(double[] dims, double[] point, double phi, double theta, double psi)
    # createBlock - Create a block of:
    #          dimensions specified in dims,
    #          centered at point,
    #          then rotated by the euler angles phi, theta, psi.    
    block=nm.MultiPlaneShape.createBlock([20.0e-6,20.0e-6,20.0e-6],[0.0,0.0,10.0e-6],0.0,0.0,0.0)
    matrix=monte.addSubRegion(monte.getChamber(),cu,block)
    for b in blocks:
      monte.addSubRegion(matrix,pd,nm.MultiPlaneShape.createBlock([sc*b[3],sc*b[3],sc*b[3]],[sc*b[0],sc*b[1],sc*b[2]],0.0,0.0,0.0))
    det.reset()
    # add an x-ray event listener
    if charF:
      xrel=nm.XRayEventListener2(monte,det)
      monte.addActionListener(xrel)
    if bremF:
      brel = nm.BremsstrahlungEventListener(monte,det)
      monte.addActionListener(brel)
    monte.runMultipleTrajectories(nTraj)
    res.seek(x+32,y+32)
    spec=wrap(epq.SpectrumUtils.addNoiseToSpectrum(det.getSpectrum(dose*1.0e-9 / (nTraj * epq.PhysicalConstants.ElectronCharge)),1.0))
    cor = spec.applyLLT()
    fix = wrap(epq.SpectrumUtils.remap(wrap(cor), 0.0, cw))
    fix.rename("remapped")
    
    # write to Ripple file
    res.write(epq.SpectrumUtils.toDoubleArray(fix))
    if (x%16==0) and (y%16==0):
      props=fix.getProperties()
      props.setTextProperty(epq.SpectrumProperties.SpectrumDisplayName, "Pixel[%d,%d]" % (x,y))
      props.setNumericProperty(epq.SpectrumProperties.LiveTime, lt)
      props.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
      props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
      display(fix)
      
# append spectrum calibration information to the .rpl file
f=open(rplFil, 'a')
strLine = 'ev-per-chan\t%.4f\n' % (cw)
f.write(strLine)
strLine = 'detector-peak-width-ev\t%.1f\n' % (resn)
f.write(strLine)
f.close()

# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"