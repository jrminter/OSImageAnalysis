# Demonstrates how to load a ripple/raw file as an object called rr
# Author: Nicholas W. M. Ritchie
# Date:   15-May-2008
deadFrac=0.3
stride=8
# First create a SpectrumProperties object with the information necessary 
# to perform a quant on the resulting spectrum.
path="/Volumes/nritchie/My Documents/2008/12-December/K411 sphere maps/10 keV/%s"
det=findDetector("Bruker 10")
sp=epq.SpectrumProperties()
sp.setDetector(det)
sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy,10.0)
sp.setNumericProperty(epq.SpectrumProperties.FaradayBegin,2.19)
sp.setNumericProperty(epq.SpectrumProperties.LiveTime,0.001*(1.0-deadFrac))
rr=ept.RippleSpectrum(path % "K411 sphere #11.rpl",sp)
rr.setSpan(stride,stride)

k411 = epq.EMSAFile().open(path % "K411 std.msa")

stds = { epq.Element.Fe : epq.EMSAFile().open(path % "Fe std.msa"),
		  epq.Element.Ca : epq.EMSAFile().open(path % "Fluoroapatite std.msa"),
		  epq.Element.Mg : epq.EMSAFile().open(path % "Mg std.msa"),
		  epq.Element.O : epq.EMSAFile().open(path % "MgO std.msa"),
		  epq.Element.Si : epq.EMSAFile().open(path % "Si std.msa")
		  }

fams = { epq.Element.Fe : [ epq.XRayTransitionSet(epq.Element.Fe,epq.XRayTransitionSet.K_FAMILY), epq.XRayTransitionSet(epq.Element.Fe,epq.XRayTransitionSet.L_FAMILY) ],
		  epq.Element.Ca : [ epq.XRayTransitionSet(epq.Element.Ca,epq.XRayTransitionSet.K_FAMILY)],
		  epq.Element.Mg : [epq.XRayTransitionSet(epq.Element.Mg,epq.XRayTransitionSet.K_FAMILY)],
		  epq.Element.O : [epq.XRayTransitionSet(epq.Element.O,epq.XRayTransitionSet.K_FAMILY)],
		  epq.Element.Si : [epq.XRayTransitionSet(epq.Element.Si,epq.XRayTransitionSet.K_FAMILY)]
		  }

mats = { epq.Element.Fe : epq.MaterialFactory.createPureElement(epq.Element.Fe),
		  epq.Element.Ca : epq.MaterialFactory.getMaterial(epq.MaterialFactory.Chloroapatite),
		  epq.Element.Mg : epq.MaterialFactory.createPureElement(epq.Element.Mg),
		  epq.Element.O : epq.MaterialFactory.createCompound("MgO"),
		  epq.Element.Si : epq.MaterialFactory.createPureElement(epq.Element.Si)
		  }

ff2=epq.FilterFit2(det)
for elm in stds:
   rois=epq.RegionOfInterestSet(det.getDetectorLineshapeModel(),0.001)
   for xrts in fams[elm]:
      rois.add(xrts)
   ff2.addReference(rois,stds[elm])
root=path % "K411 sphere #11 k-ratios.%s"   
resFile = ept.RippleFile(rr.getCols() % stride, rr.getHeight() % stride, 5, ept.RippleFile.FLOAT, 4, epq.RippleFile.VECTOR_ORDER, root % "rpl", root % "raw") 
for row in range(0,rr.getRows() % stride):
	for col in range(0,rr.getCols() % stride):
		rr.setPosition(row,col)
		krs=ff2.getResult(rr)
		tmp=[]
		for elm in stds:
			tmp=tmp+[krs.getKRatio(fams[elm][0])]
		resFile.setPosition(row,col)
		resFile.write(tmp)