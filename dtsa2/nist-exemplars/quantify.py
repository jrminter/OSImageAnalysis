
class Quantify:
	"""A simple wrapper around epq.QuantifyUsingStandards to simplify use."""
	
	def __init__(self, det, e0):
		assert isinstance(det, epq.EDSDetector), "%s is not an EDS detector" % det
		assert (e0>1.0) and (e0<50.0), "The beam energy is outside of the range [1.0 keV, 50.0 keV]"
		self.quant = epq.QuantifyUsingStandards(det, epq.ToSI.keV(e0))
		
	def addStandard(self, elm, comp, spec):
		assert isinstance(comp,epq.Composition) , "%s is not a composition." % comp
		assert isinstance(elm,epq.Element), "%s is not an element." % elm
		assert isinstance(spec,epq.ISpectrumData), "%s is not a spectrum." % spec
		assert comp.containsElement(elm), "%s does not contain %s." % (comp, elm)
		self.quant.addStandard(elm, comp, spec)
		
	def setStrippedElement(self, elm):
		assert isinstance(epq.Element, elm), "%s is not an element." % elm
		self.quant.addElementToStrip(elm)
		
	def getMissingReferences(self):
		return self.quant.getMissingReferences()	
	
	def setOxygenByStoichiometry(self):
		self.quant.addUnmeasuredlementRule(epq.CompositionFromKRatios.ElementByStoichiometry.OxygenByStoichiometry(0))
	
	def addReference(self, roi, spec):
		assert isinstance(roi, epq.RegionOfInterestSet) or isinstance(roi, epq.RegionOfInterestSet.RegionOfInterest), "%s must be a region-of-interest or a region-of-interest set."
		assert isinstance(spec,epq.ISpectrumData), "%s is not a spectrum." % spec
		self.quant.addReference(roi, spec)
		
	def compute(self, unknown):
		assert isinstance(unknown, epq.ISpectrumData), "%s is not a spectrum." % unknown