# 0_makeMsas.py
#
# 2014-03-31 J. R. Minter 
# Make MSA files to test quantify
#
import os
import shutil
import java.io as jio
import dtsa2.jmGen as jmg

git = os.environ['GIT_HOME']
# the project directory
wd = git + "/OSImageAnalysis/dtsa2/other-macros/testScripts"
os.chdir(wd)
pyrDir = wd + "/0_makeMsas Results/"

DataManager.clearSpectrumList()
spcDir = git + "/OSImageAnalysis/dtsa2/spc/"
msaDir = git + "/OSImageAnalysis/dtsa2/msa/"

sDet    = "FEI FIB620 EDAX-RTEM"
det     = findDetector(sDet)
pc      = 1.0
wrkDist = 17.2 # mm
vkV     = [15]
end     = 1200

for e0 in vkV:
  cuFil = spcDir + "Cu-%g-1.spc" % e0
  raw = readSpectrum(cuFil, i=0, det=det)
  lt = raw.liveTime()
  cuStdSpc = jmg.cropSpec(raw, start=0, end=end)
  props = cuStdSpc.getProperties()
  props.setDetector(det)
  props.setTextProperty(epq.SpectrumProperties.SpecimenName, "Cu Grid")
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  props.setNumericProperty(epq.SpectrumProperties.WorkingDistance, wrkDist)
  cuStdSpc.setLiveTime(lt)
  cuStdSpc.setProbeCurrent(pc)
  cuStdSpc.setAsStandard(epq.Composition(epq.Element.Cu))
  cuStdSpc.rename("CuStd")  
  display(cuStdSpc)
  # set up the standard
  print(cuStdSpc.getChannelCount())
  display(cuStdSpc)
  cuStdFil = msaDir + "Cu-%g-Std.msa" % e0
  fos=jio.FileOutputStream(cuStdFil)
  ept.WriteSpectrumAsEMSA1_0.write(cuStdSpc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
  fos.close()
  
  cuFil = spcDir + "Cu-%g-2.spc" % e0
  raw = readSpectrum(cuFil, i=0, det=det)
  lt = raw.liveTime()
  cuSpc = jmg.cropSpec(raw, start=0, end=end)
  props = cuSpc.getProperties()
  props.setDetector(det)
  props.setTextProperty(epq.SpectrumProperties.SpecimenName, "Cu Grid")
  props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
  props.setNumericProperty(epq.SpectrumProperties.WorkingDistance, wrkDist)
  cuSpc.setLiveTime(lt)
  cuSpc.setProbeCurrent(pc)
  cuSpc.rename("CuUnk")
  display(cuSpc)
  print(cuSpc.getChannelCount())
  display(cuSpc)
  cuUnkFil = msaDir + "Cu-%g-Unk.msa" % e0
  fos=jio.FileOutputStream(cuUnkFil)
  ept.WriteSpectrumAsEMSA1_0.write(cuSpc,fos,ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
  fos.close()


# clean up cruft
shutil.rmtree(pyrDir)
print "Done!"
