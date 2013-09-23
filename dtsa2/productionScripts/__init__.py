# -*- coding: utf-8 -*-
# Title: initialize.py
# Description:  The initialization script that executes each time DTSA2
#   starts the command prompt. This script provides the core command line
#   spectrum analysis functionality.
# Author: Nicholas W. M. Ritchie

"""DTSA-II is an open source application for quantification and simulation of microanalysis experiments. \
DTSA-II provides a GUI to simplify common operations and a scripting interface to implement more sophisticated functionality. \
The scripting interface is based on a Java implementation of the Python language called Jython.
+ Type 'dir()' to get a list of global classes and methods or dir(package) for a list of methods and classes within package.  
+ Type 'help(item)' for basic assistance on the class, function or method identified by name as item.
+ For help with the important class ScriptableSpectrum, type 'help(ScriptableSpectrum)'.
+ JRM Note: N.B. This has the change to multiQuant N. Ritchie sent me on 2013-09-23.
+ Goes in ...DTSA-II-Gemini/Lib/dtsa2/"""

__revision__ = "$Id: __init__.py Nicholas W. M. Ritchie $"
__version__ = "0.0.1"

import gov.nist.microanalysis.EPQLibrary as epq
import gov.nist.microanalysis.EPQTools as ept
import gov.nist.microanalysis.Utility as epu
# This next two lines of weirdness eliminate a "no module named" error.  Why????
import sys as sys
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte", "MonteCarloSS", None)
import gov.nist.microanalysis.NISTMonte as nm
import gov.nist.microanalysis.dtsa2 as dt2
import gov.nist.microanalysis.EPQLibrary.Detector as epd
import java.lang as jl
import java.io as jio
import java.util as ju
import jarray

import edu.stanford.ejalbert.BrowserLauncher as bl

App = dt2.DTSA2.getInstance()
MainFrame = App.getFrame()
Database = dt2.DTSA2.getSession()
DefaultOutput = (globals()["DefaultOutput"] if globals().has_key("DefaultOutput") else None)
DataManager = dt2.DataManager.getInstance()
StdOut = MainFrame.getStandardOutput()
StdErr = MainFrame.getStandardError()
terminated = False

# A basic set of default standard materials.
defaultStandards = { "O":"SiO2", "Ba":"BaF2", "F":"CaF2", "N":"BN", "Na":"NaCl", "S":"FeS2", "Cl":"NaCl", "K":"KCl", "Ca":"CaF2", "Br":"KBr",
                    "Pb":"K227", "U":"U2O3", "Hg":"HgTe" }


def run(script):
   """run(script)
   Runs the script in the file specified by script."""
   MainFrame.runPythonScript(script)

def execute(cmd):
    """execute(cmd)
    Passes a command to the operating system to execute in a separate process"""
    pb = jl.ProcessBuilder([cmd])
    p = pb.start()

def reportPath():
   """reportPath()
   Returns the directory into which the report and associated data is being written."""
   return App.getReport().getFile().getParent()

# Overloads the operators +,- and * to use spectrum math...
class ScriptableSpectrum(epq.BaseSpectrum):
    """Class ScriptableSpectrum:
    Defines operators and methods for working with spectrum objects from within the command line environment.  ScriptableSpectrum objects may be added (s1+s2), subtracted (s1-s2), multiplied (2.0*s1 or s1*2.0) or you may apply methods to ScriptableSpectrum objects. All the objects listed by a call to ls() are ScriptableSpectrumobjects.  Type 'dir(ScriptableSpectrum)' to get a list of methods or 'help(ScriptableSpectrum.getCounts)' or similar to get help on a method."""
    def __init__(self, arg):
        # Don't multiply wrap spectra
        if isinstance(arg, ScriptableSpectrum):
            self.wrapped = arg.wrapped
        else:
            self.wrapped = arg

    def __add__(self, other):
        res = epq.SpectrumMath(self.wrapped)
        if other != None:
            res.add(other, 1.0)
        return ScriptableSpectrum(res)

    def __sub__(self, other):
        res = epq.SpectrumMath(self.wrapped)
        if other != None:
            res.subtract(other, 1.0)
        return ScriptableSpectrum(res)

    def __mul__(self, other):
        return ScriptableSpectrum(epq.SpectrumUtils.scale(other, self.wrapped))

    def __rmul__(self, other):
        return ScriptableSpectrum(epq.SpectrumUtils.scale(other, self.wrapped))

    def __repr__(self):
        return self.wrapped.toString()
    
    def __getitem__(self, key):
        return self.wrapped.getCounts(key)

    def __len__(self):
        return self.wrapped.getChannelCount()
    
    def __str__(self):
        return self.wrapped.toString()

    def abs(self):
        """s.abs()
    Returns the absolute value of the channel data"""
        return ScriptableSpectrum(epq.SpectrumUtils.getAbsSpectrum(self.wrapped))

    def positiveDefinite(self):
        """s.positiveDefinite()
    Returns the spectrum with any negative channel data points set to zero."""
        return ScriptableSpectrum(epq.SpectrumUtils.getPositiveSpectrum(self.wrapped))

    def getChannelCount(self):
        """s.getChannelCount()
    Returns the number of channels in the spectrum."""
        return self.wrapped.getChannelCount()

    def getCounts(self, ch):
        """s.getCounts(ch)
    Returns the number of x-ray event counts in channel ch or in a range of channels"""
        if isinstance(ch, slice):
            return sum(self.wrapped.getCounts(i) for i in range(*ch.indices(self.getChannelCount())))
        else:
            return self.wrapped.getCounts(ch)

    def getChannelWidth(self):
        """s.getChannelWidth()"""
        return self.wrapped.getChannelWidth()

    def getZeroOffset(self):
        """s.getZeroOffset()"""
        return self.wrapped.getZeroOffset()

    def getProperties(self):
        """s.getProperties()
    Returns the SpectrumProperties object associated with the spectrum s."""
        return self.wrapped.getProperties()

    def getWrapped(self):
        """s.getWrapped()
    Returns the base Java spectrum from which this ScritableSpectrum was created."""
        return self.wrapped

    def rename(self, name):
        """s.rename('name')
    Changes the display name of the spectrum s to name"""
        epq.SpectrumUtils.renameSpectrum(self.wrapped, name)
        MainFrame.updateDisplayedSpectra();

    def display(self):
        """s.display()
    Adds this spectrum to the SpectrumList and displays it in the spectrum display"""
        display(self.wrapped)

    def property(self, name):
        """s.property(name)
    Returns the spectrum property associated with the specified display name."""
        return self.wrapped.getProperties().getPropertyByName(name)

    def toString(self):
        """s.toString()
    Returns the display name for this spectrum."""
        return self.wrapped.toString()

    def scale(self, k):
        """s.scale(0.8)
    Scale this spectrum by the specified amount."""
        return ScriptableSpectrum(epq.SpectrumUtils.scale(k, self.wrapped))

    def maxChannel(self):
        """s.maxChannel()
    Return the index of the maximum valued channel in the specified spectrum."""
        return epq.SpectrumUtils.maxChannel(self.wrapped)

    def firstNonZeroChannel(self):
        """s.firstNonZeroChannel()
    Returns the first channel containing a non-zero value."""
        return epq.SpectrumUtils.firstNonZeroChannel(self.wrapped)

    def lastNonZeroChannel(self):
        """s.lastNonZeroChannel()
    Returns the last channel containing a non-zero value."""
        return epq.SpectrumUtils.lastNonZeroChannel(self.wrapped)

    def peakIntegral(self, e0, e1):
        """s.peakIntegral(e0,e1)
    Computes the background corrected peak integral for the range of channels between e0 and e1."""
        res = epq.SpectrumUtils.backgroundCorrectedIntegral(self.wrapped, e0, e1)
        return epu.UncertainValue(res[0], res[1])

    def toDouble(self):
        """s.toDouble()
    Converts the spectrum channel data to an array of double values."""
        return epq.SpectrumUtils.toDoubleArray(self.wrapped)

    def energies(self):
        """s.energies()
    Returns an array of energies corresponding to the average energy in each channel"""
        return epq.SpectrumUtils.energyArray(self.wrapped)

    def subSample(self, k):
        """s.subSample(k)
    Returns a statistically valid sub-sampling of the spectrum s for an assumed live time of k seconds where k<s.liveTime()"""
        return wrap(epq.SpectrumUtils.subSampleSpectrum(self.wrapped, k))
  
    def partition(self, n=10):
        """s.partition(n)
    Subdivides the counts in one spectrum into n spectra in a manner equivalent to if the n specta represent n equal time segments which sum to the total acquisition time."""
        res = epq.SpectrumUtils.partition(self.wrapped, n)
        rr = []
        for s in res:
            rr = rr + [wrap(s)]
        return rr

    def totalCounts(self):
        """s.totalCounts()
    Returns the total number of counts in all channels of the spectrum s."""
        return epq.SpectrumUtils.totalCounts(self.wrapped)

    def liveTime(self):
        """s.liveTime()
    Returns the live time (in seconds) associated with the spectrum s. Returns -1.0 if the live time is not specified."""
        return self.wrapped.getProperties().getNumericWithDefault(epq.SpectrumProperties.LiveTime, - 1.0)

    def setLiveTime(self, lt):
        """s.setLiveTime(lt)
    Sets the live time associated with the spectrum s to lt seconds"""
        self.wrapped.getProperties().setNumericProperty(epq.SpectrumProperties.LiveTime, lt)

    def probeCurrent(self):
        """s.probeCurrent()
    Returns the average probe current in nA as reported by this spectrum.  If the probe current is not defined then this method returns -1.0"""
        return epq.SpectrumUtils.getAverageFaradayCurrent(self.wrapped.getProperties(), - 1.0)

    def setProbeCurrent(self, pc):
        """s.setProbeCurrent(0.5)
    Sets the probe current to the specified value in nA."""
        p = self.wrapped.getProperties()
        p.setNumericProperty(epq.SpectrumProperties.FaradayBegin, pc)
        if p.isDefined(epq.SpectrumProperties.FaradayEnd):
            p.setNumericProperty(epq.SpectrumProperties.FaradayEnd, pc)
            
    def beamEnergy(self):
        """s.beamEnergy()
    Returns the beam energy (in keV) associated with the spectrum s."""
        return epq.SpectrumUtils.getBeamEnergy(self.wrapped) / 1000.0

    def takeOffAngle(self):
        """s.takeOffAngle()
    Returns the take-off angle (in degrees) associated with the spectrum s"""
        return jl.Math.toDegrees(epq.SpectrumUtils.getTakeOffAngle(self.wrapped.getProperties()))

    def smooth(self):
        """s.smooth()
    Performs a fifth-order Savitzky-Golay filter on the spectrum s."""
        return ScriptableSpectrum(epq.SpectrumSmoothing.SavitzkyGolay5.compute(self.wrapped))
    
    def duaneHunt(self):
        """s.duaneHunt()
    Computes the Duane-Hunt limit in keV for the spectrum s"""
        return epq.FromSI.keV(epq.DuaneHuntLimit.LinearDuaneHunt.compute(self.wrapped))

    def setAsStandard(self, comp):
        """s.setAsStandard(comp)
    Specify that the spectrum s is a standard with the composition specified in comp"""
        self.getProperties().setCompositionProperty(epq.SpectrumProperties.StandardComposition, comp)

    def backgroundCorrect(self):
        """s.backgroundCorrect()
    Remove the modeled Bremsstrahlung background from this spectrum and return the resulting spectrum."""
        p = self.getProperties()
        try:
            det = p.getDetector()
        except epq.EPQException:
            CommandLine.writeException("The backgroundCorrect method requires the \"Detector\" spectrum property")
        c = p.getCompositionWithDefault(epq.SpectrumProperties.StandardComposition, None)
        if c == None:
            c = p.getCompositionWithDefault(epq.SpectrumProperties.MicroanalyticalComposition, None)
        if c == None:
            c = createMaterial()
        if c != None:
            self.setAsStandard(c)
        if c == None:
            raise Exception("backgroundCorrect: No material specified for %s" % self.toString())
        ba = epq.BremsstrahlungAnalytic.DTSA
        return self - ScriptableSpectrum(ba.fitBackground(det, self.wrapped, c))

    def setFWHMatMnKa(self, fwhm):
       """s.setFWHMatMnKa(fwhm)
       Set the FWHM at Mn Ka to the specified value in eV."""
       p = self.getProperties();
       p.setNumericProperty(epq.SpectrumProperties.Resolution, fwhm)
       p.getNumericWithDefault(epq.SpectrumProperties.ResolutionLine, epq.SpectrumUtils.E_MnKa)
        
    def getFWHMatMnKa(self, defFwhm):
        return epq.SpectrumUtils.getFWHMAtMnKA(self, defFwhm)

    def save(self, filename):
        """s.save(filename)
    Write this spectrum to an EMSA 1.0 format text file."""
        os = jio.FileOutputStream(filename)
        ept.WriteSpectrumAsEMSA1_0.write(self.wrapped, os, ept.WriteSpectrumAsEMSA1_0.Mode.COMPATIBLE)
        os.close()

    def toXML(self, filename):
        """s.toXML(filename)
    Convert this spectrum to a proprietary but full fidelity XML format. spectrumFromXML(filename), the inverse method, is a global function."""
        os = jio.FileOutputStream(filename)
        self.wrapped.toXML(os)
        os.close()

    def __getslice__(self, low, high):
        """s.slice(lowCh,highCh)
    Creates a spectrum containing only the data in channels between lowCh (inclusive) and highCh (exclusive)"""
        return epq.SpectrumUtils.slice(self.wrapped, low, high)

    def autoOffset(self):
        """s.autoOffset()
    Offset the spectrum channel data so that the minimum channel equals zero counts."""
        return wrap(epq.SpectrumUtils.scale(1.0, - self.getCounts(epq.SpectrumUtils.minChannel(self)), self))

    def offset(self, off):
        """s.offset(100.0)
    Offset the spectrum channel data up by the specified number of counts."""
        return wrap(epq.SpectrumUtils.scale(1.0, off, self.wrapped))

    def remap(self, zero, chWidth):
        """s.remap(-100.0,10.0)
    Returns a new spectrum which is similar to this one except that the zero offset and channel width have been remapped to the specified values."""
        return wrap(epq.SpectrumUtils.remap(self.wrapped, zero, chWidth))

    def remap(self, det):
        """s.remap(det)
    Returns a new spectrum which is similar to this one except that the zero offset and channel width have been remapped to be same as the specified detector."""
        res = epq.SpectrumUtils.remap(self.wrapped, det.getZeroOffset(), det.getChannelWidth())
        res.getProperties().setDetector(det)
        return wrap(res)

    def applyLLT(self):
        """s.applyLLT()
    Returns a new spectrum which is similar to this one except that all channels below the energy identified by the ZeroPeakDiscriminator property as set to zero."""
        return wrap(epq.SpectrumUtils.applyZeroPeakDiscriminator(self.wrapped))
   
    def composition(self, prop=epq.SpectrumProperties.MicroanalyticalComposition):
        """s.composition()
    Returns the composition of the specified spectrum if one is associated."""
        return self.getProperties().getCompositionWithDefault(prop, None)
    
    def channel(self, energy):
        '''channel(129.0)
        Returns the channel associated with the specified energy in eV.'''
        return epq.SpectrumUtils.channelForEnergy(self.wrapped, energy)
    
    def energy(self, channel):
        '''energy(channel)
        Returns the energy associated with the specfied channel.'''
        return epq.SpectrumUtils.minEnergyForChannel(self.wrapped, channel)

def spectrumFromXML(filename):
   """spectrumFromXML(filename)
   Read a spectrum from a file saved using the ScriptableSpectrum.toXML(...) method. \
   Returns a ScriptableSpectrum object."""
   input = jio.FileInputStream(filename)
   res = epq.BaseSpectrum.fromXML(input)
   input.close()
   return wrap(res)

PathSep = jl.System.getProperty("file.separator")

def parseChemicalFormula(formula, density=0.0):
   """parseChemicalFormula('CaCO3',[density=2.71])
   Create a Material (or Composition if density omitted) object by parsing the chemical formula in the argument"""
   if density > 0.0:
      return epq.MaterialFactory.createCompound(formula, epq.ToSI.gPerCC(density))
   else:
      return epq.MaterialFactory.createCompound(formula)
  
def material(name, density=0.0):
   '''material("TiO2",[density=4.27])
The function creates a Composition object by first checking \
the material database for a material with the specified name. \
If the material isn't in the database it will then attempt to \
parse the name as a chemical formula.  If both of these fail \
the method will return None.'''
   if isinstance(name, epq.Composition) or isinstance(name, epq.Material):
      res = name
      if density > 0.0:
         res = epq.Material(name, epq.ToSI.gPerCC(density))
      return res
   res = dt2.DTSA2.getSession().findStandard(name)
   if not res:
      res = parseChemicalFormula(name, density)
   if (density > 0.0) and res:
      res = epq.Material(res, epq.ToSI.gPerCC(density))
   return res

def addTrace(m, elm, qty, norm=True):
    """addTrace(m, elm, qty, [norm=True]) Add a trace amount qty (in mass fraction) of elm to the material m.  Normalize \
the result to 1.0 if norm=True otherwise just add qty of elm to the analytical total."""
    m = material(m)
    elm = element(elm)
    name = "%s + %g %s" % ( m.toString(), qty, elm.toAbbrev())
    n = (1.0 - qty if norm else 1.0)
    if m.containsElement(elm):
        qty=qty+m.weightFraction(elm,norm)*n
    elms, qtys = [ elm, ], [qty, ]
    for z in m.getElementSet():
        if not z.equals(elm):
            elms.append(z)
            qtys.append(m.weightFraction(z, norm)*n)
    res = epq.Composition(elms, qtys)
    if isinstance(m, epq.Material):
        res = epq.Material(res, m.getDensity())
    res.setName(name)
    return res

def element(name):
   """element('Si')
   Parses the argument string and returns the associated Element object."""
   if isinstance(name, str):
      return epq.Element.byName(name)
   else:
      return name

def elements(listOfElms):
   """elements(['Si','Fe','Na', epq.Element.Tb])
   Parses the argument string and returns the associated list of Element objects."""
   res = []
   for elm in listOfElms:
      res.append(element(elm))
   return res

def atomicShell(shell):
   """atomicShell('Si-K')
   Parses the argument string and returns the associated AtomicShell object."""
   return (shell if isinstance(shell, epq.AtomicShell) else epq.AtomicShell.parseString(shell))

def transition(tr):
   """transition('Si K-LIII')
   Parses the argument string and returns the associated XRayTransition object."""
   return (tr if isinstance(tr, epq.XRayTransition) else epq.XRayTransition.parseString(tr))

def listTransitions(elmName):
   """listTransitions('Si')
   Lists all x-ray transitions associated with the element specified by abbreviation or name."""
   elm = element(elmName)
   print "IUPAC\tSiegbahn\tWeight\tEnergy\tWavelength"
   print u"     \t        \t     \t(keV) \t  (\u212B)"
   try:
      for xrt in range(epq.XRayTransition.KA1, epq.XRayTransition.N5N6 + 1):
         if epq.XRayTransition.exists(elm, xrt):
            tr = epq.XRayTransition(elm, xrt)
            print "%s\t%s\t%g\t%g\t%g" % (tr.toString(), tr.getSiegbahnName(), tr.getWeight(epq.XRayTransition.NormalizeKLM), epq.FromSI.keV(tr.getEnergy()), 1.0e10 * epq.SpectrumUtils.energyToWavelength(tr.getEnergy()))
   except jl.IllegalArgumentException:
      pass

def listEdges(elmName, alg=epq.EdgeEnergy.Chantler2005):
   """listEdge('Si',[alg=epq.EdgeEnergy.Chantler2005])
   Lists all absorption edges associated with the element specified by abbreviation or name."""
   elm = element(elmName)
   print "IUPAC\tSiegbahn\tEnergy\tJump\tIon..\tFluor"
   print "\t\t(keV)\tRatio\tFrac.\tYield"
   try:
       jr = epq.JumpRatio.Springer1967
       fy = epq.FluorescenceYield.ENDLIB97
       for ee in range(epq.AtomicShell.K, epq.AtomicShell.QXIII + 1):
           at = epq.AtomicShell(elm, ee)
           if alg.isSupported(at):
               print "%s\t%s\t%g\t%0.4f\t%0.4f\t%0.4f" % (at.toString(), at.getSiegbahnName(), epq.FromSI.keV(alg.compute(at)), jr.compute(at), jr.ionizationFraction(at), fy.compute(at))
   except jl.IllegalArgumentException:
       pass

def listData(elmName):
   """listData('Si')
   Lists element data, edge energies and x-ray transitions associated with the element specified by abbreviation or name."""
   elm = element(elmName)
   print "Abbrev\tName\tZ\tA"
   print "%s\t%s\t%d\t%g" % (elm.toAbbrev(), elm.toString(), elm.getAtomicNumber(), elm.getAtomicWeight())
   print
   listEdges(elmName)
   print
   listTransitions(elmName)

def ls():
   """ls()
   List the spectra in the Spectrum List and their Jython alias."""
   if DataManager.isEmpty():
      print "No spectra"
   else:
      print "Name\tSpectrum"
      print DataManager.listSpectra()

def listSpectra():
   """listSpectra()
   List the spectra in the Spectrum List and their Jython alias.  Same as ls()"""
   ls()

def clear():
   """clear()
   Unselect all spectra in the Spectrum List.  They won't be displayed in the spectrum display."""
   DataManager.clearSelections()

def displayAll():
   """displayAll()
   Display all spectra in the spectrum list on the spectrum display."""
   DataManager.setSelected(DataManager.spectrumList())

def selected():
   """selected()
   Return a list of all spectra selected in the Spectrum List."""
   return DataManager.getSelected()

def spectra(selectedOnly=False):
   """spectra([selectedOnly=False])
   Return a list of all spectra in the Spectrum List."""
   if selectedOnly:
      return DataManager.getInstance().getSelected()
   else:
      return DataManager.spectrumList()

def run(filename):
   """run('/usr/home/script.py')
   Execute the specified script."""
   MainFrame.runPythonScript(filename)

def rerun():
   """rerun()
   Reexecute the last script."""
   MainFrame.rerunPythonScript()

def editMaterial(comp):
   """editMaterial(mat)
   Edit the Material object specified by mat using the material editor dialog."""
   return MainFrame.editMaterial(comp)

def createMaterial():
   """createMaterial()
   Create a new Material object using the material editor dialog."""
   return MainFrame.createMaterial()

def getElement(exclude=[]):
   """getElement() or getElement([epq.Element.H, epq.Element.He])
   Displays a dialog from which to select one element."""
   se = ept.SelectElements(MainFrame, "Select an element", True)
   se.setLocationRelativeTo(MainFrame)
   se.setMultiSelect(False)
   for elm in exclude:
      se.setEnabled(element(elm), 0)
   se.setVisible(True)
   elms = se.getElements()
   if elms.size() == 1:
      return elms.iterator().next()
   else:
      return None

def getElements(elms=[], exclude=[]):
   """editElements([epq.Element.Fe, epq.Element.Ni],[epq.Element.H, epq.Element.He])
   Displays a periodic table dialog from which to select a list of elements.  Elements in the second list are excluded from list of selectable elements."""
   se = ept.SelectElements(MainFrame, "Select some elements", True)
   se.setLocationRelativeTo(MainFrame)
   se.setMultiSelect(True)
   se.setSelected(elements(elms))
   for elm in exclude:
      se.setEnabled(element(elm), 0)
   se.setVisible(True)
   return se.getElements()

def listDetectors():
   """listDetectors()
   Displays a list of variable names and the associated detector definition object."""
   print "Name\tDetector"
   for me in Database.getDetectorsInt().entrySet():
      print "d%d\t%s" % (me.getValue(), me.getKey().toString())

def majorTransitions(comp, e0, trs=(epq.XRayTransition.KA1, epq.XRayTransition.KB1, epq.XRayTransition.LA1, epq.XRayTransition.MA1), thresh=1.0):
   """majorTransitions(comp,e0,[trs],[thresh=1.0])
   Returns a list of all major transitions present for the specified composition at the specified beam energy (e0)"""
   xrts = []
   for elm in comp.getElementSet():
      for tr in trs:
         if epq.XRayTransition.exists(elm, tr):
            eTr = epq.FromSI.keV(epq.XRayTransition.getEnergy(elm, tr))
            if (eTr > 0.05) and (eTr < thresh * e0):
               xrts.append(epq.XRayTransition(elm, tr))
   return xrts

def majorTransitionSets(det, comp, e0):
   """majorTransitionSets(det, comp, e0)
   Returns a list of the sets of transitions associated with the elements in this material"""
   dlsm = det.getDetectorLineshapeModel()
   fwhm = epq.ToSI.eV(dlsm.getFWHMatMnKa())
   rois = epq.RegionOfInterestSet(dlsm, 0.0, 0.5 * fwhm, 0.5 * fwhm)
   for elm in comp.getElementSet():
      rois.add(elm, epq.ToSI.keV(e0), 0.0)
   res = []
   for elm in comp.getElementSet():
      for roi in rois:
         xrts = roi.getXRayTransitionSet(elm)
         if xrts.size() > 0:
            res.append(xrts)
   return res


def zaf(comp, det, e0, alg=epq.XPP1991(), mac=epq.MassAbsorptionCoefficient.Chantler2005, xtra=epq.SpectrumProperties(), stds=None, mode="WDS"):
   """zaf(comp, d1, 20.0, [alg=epq.XPP1991()], [mac=epq.MassAbsorptionCoefficient.Henke1993], [xtra=epq.SpectrumProperties()],[stds=None],[mode="WDS"|"EDS"|"EXHAUSTIVE"])
   Display the ZAF correction associated with the specified composition (comp),  detector (d1) and beam energy (20.0) using the correction algorithm specified.  If no algorithm is specified then Pouchou and Pichoir's XPP algorithm is used. \
   If you don't specify stds then pure elements are assumed.  Otherwise standards is a dictionary mapping an element to a composition."""
   comp = material(comp)
   if (comp <> None) and (comp.getElementCount() > 0):
      oldStrat = epq.AlgorithmUser.getGlobalStrategy()
      s = epq.Strategy()
      s.addAlgorithm(epq.MassAbsorptionCoefficient, mac)
      epq.AlgorithmUser.applyGlobalOverride(s)
      props = epq.SpectrumProperties()
      props.setDetector(det)
      props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
      props.addAll(xtra)
      print "Material\t%s" % (comp.descriptiveString(0))
      print "Detector\t%s" % det
      print "Algorithm\t%s" % alg.getName()
      print "MAC\t%s" % alg.getAlgorithm(epq.MassAbsorptionCoefficient).getName()
      print "E0\t%g keV" % props.getNumericProperty(epq.SpectrumProperties.BeamEnergy)
      print "Take-off\t%g%s" % (jl.Math.toDegrees(epq.SpectrumUtils.getTakeOffAngle(props)), epq.SpectrumProperties.TakeOffAngle.getUnits())
      for sp in xtra.getPropertySet():
          print "%s\t%s" % (sp, xtra.getTextProperty(sp))
      if stds:
          conv = {}
          for z, c in stds.iteritems():
              conv[element(z)] = material(c)
          stds = conv
      mode=mode.lower()
      if mode.startswith("w") or mode.startswith("ex"):
         print "\nIUPAC\tSeigbahn\tStandard\tEnergy\t ZAF\t  Z\t  A\t  F\tk-ratio"
         mtr=(majorTransitions(comp, e0, thresh=0.8) if mode.startswith("w") else majorTransitions(comp,e0,epq.XRayTransition.ALL_TRANSITIONS,0.99))
         for xrt in mtr:
            try:
               elm = xrt.getElement()
               std = (stds.get(elm) if stds else None)
               if std:
                   ww = std.weightFraction(elm, False)
                   zaf = alg.relativeZAF(comp, xrt, props, std)
               else:
                   ww = 1.0
                   zaf = alg.relativeZAF(comp, xrt, props)
               k = zaf[3] * comp.weightFraction(elm, False) / ww
               eTr = epq.FromSI.keV(xrt.getEnergy())
               print "%s\t%s\t%s\t%2.4f\t%1.4f\t%1.4f\t%1.4f\t%1.4f\t%1.4f" % (xrt, xrt.getSiegbahnName(), (std if std else "Pure %s" % elm.toAbbrev()), eTr, zaf[3], zaf[0], zaf[1], zaf[2], k)
            except jl.Throwable:
               pass
      else:
         print "\n%-15s\tStandard\tEnergy\t ZAF\t  Z\t  A\t  F\tk-ratio" % "IUPAC"
         for xrts in majorTransitionSets(det, comp, e0):
            z, a, f, zaf, w = 0.0, 0.0, 0.0, 0.0, 0.0
            elm = xrts.getElement()
            std = (stds.get(elm) if stds else None)
            ww = (std.weightFraction(elm, False) if std else 1.0)
            for xrt in xrts:
               rzaf = (alg.relativeZAF(comp, xrt, props, std) if std else alg.relativeZAF(comp, xrt, props))
               wgt = xrt.getWeight(epq.XRayTransition.NormalizeFamily)
               z = z + wgt * rzaf[0] 
               a = a + wgt * rzaf[1] 
               f = f + wgt * rzaf[2] 
               zaf = zaf + wgt * rzaf[3]
               w = w + wgt
               eTr = epq.FromSI.keV(xrt.getEnergy())
            z, a, f, zaf = z / w, a / w, f / w, zaf / w
            k = zaf * comp.weightFraction(elm, False) / ww
            print "%-15s\t%s\t%2.4f\t%1.4f\t%1.4f\t%1.4f\t%1.4f\t%1.4f" % (xrts, (std if std else "Pure %s" % elm.toAbbrev()), eTr, zaf, z, a, f, k)
      # Restore previous algorithm preferences
      epq.AlgorithmUser.applyGlobalOverride(oldStrat)
      
def getEfficiency(det):
   """getEfficiency(d2).display()
   Returns the efficiency of the detector (window+crystal) as a function of energy for the specified detector as a ScriptableSpectrum object."""
   dp = det.getDetectorProperties()
   cal = det.getCalibration()
   da = dp.getProperties().getNumericWithDefault(epq.SpectrumProperties.DetectorArea, 10.0) * 1.0e-6;
   ss = epq.SpectrumUtils.toSpectrum(cal.getChannelWidth(), cal.getZeroOffset(), cal.getEfficiency(dp))
   res = ScriptableSpectrum(epq.SpectrumUtils.scale(100.0 / da, ss))
   res.getProperties().setDetector(det)
   res.rename("Efficiency[%s]" % det)
   return res

def helpStr(arg, recurse=True):
   """javaArgs(javaMethod)
   Outputs the various different call syntaxes available for the specified java method."""
   res=""
   da=dir(arg)
   # Has a doc string, return a doc string....
   if ('__doc__' in da) and (arg.__doc__ != None):
      return str(arg.__doc__)
   if ('__class__' in da):
      cn=str(arg.__class__)
      if (cn=="<type 'instancemethod'>"):
         # Java instance method, return an arglist
         res = "Java Method:"
         if "argslist" in da:
            i = 1
            for arg in arg.argslist:
               if arg != None:
                  res = "%s\n Style %d\n  %s" % (res, i, arg.data)
                  i = i + 1
         else:
            res = "%s\n No arguments: %s()" % (res, arg.__name__)
      elif(cn=="<type 'java.lang.Class'>"):
         res = "Java class: %s" % (str(arg)[7,-2])
         for m in da:
            if (not str(m).startswith("_")) and recurse:
               tmp.append(helpStr(eval("%s.%s" % (arg, m)),False))
         if len(tmp)>0:
            res = "%s\nMethods:\n\t%s" % (res,"\n\t".join(tmp))
      elif cn.startswith("<type '"):
         res = "%sInstance of Java class %s" % (res,cn[7:-2])
         tmp=[]
         for m in da:
            if (not str(m).startswith("_")) and recurse:
               tmp.append(helpStr(eval("%s.%s" % (arg, m)),False))
         if len(tmp)>0:
            res = "%s\nMethods:\n\t%s" % (res,"\n\t".join(tmp))
      elif cn.startswith("<class '"):
         res = "%sInstance of Python class %s" % (res,cn[8:-2])
         tmp=[]
         for m in da:
            if (not str(m).startswith("_")) and recurse:
               tmp.append(helpStr(eval("%s.%s" % (arg,m)),False))
         res = "%s\nMethods:\n\t%s" % (res,"\n\t ".join(tmp))
      else:
         if len(res)==0:
            res = "No help available for %s" % str(arg)
      res = res.replace("gov.nist.microanalysis.EPQLibrary", "epq")
      res = res.replace("gov.nist.microanalysis.EPQTools", "ept")
      res = res.replace("gov.nist.microanalysis.Utility", "epu")
      res = res.replace("gov.nist.microanalysis.NISTMonte", "nm")
      res = res.replace("gov.nist.microanalysis.EPQDatabase", "epdb")
      res = res.replace("gov.nist.microanalysis.dtsa2", "dt2");
      res = res.replace("gov.nist.microanalysis.EPQLibrary.Detector", "epd")
      res = res.replace("java.lang", "jl")
      res = res.replace("java.io", "jio")
   elif '__name__' in da:
      res = "%sAlias for %s" % (res,arg.__name__)
      tmp=[]
      for m in da:
         if not str(m).startswith("__"):
            tmp.append("%s" % m)
      res = "%s\nChildren:\n\t%s" % (res,", ".join(tmp))
   else:
      res = "%s\n%s" % (res,str(da))
   return res

def help(arg=None):
   """help(arg)
   Displays ?useful? information about 'arg'"""
   if arg:
      print helpStr(arg,True)
   else:
      print __doc__

def wrap(s):
   """wrap(s)
   Convert a spectrum to a ScriptableSpectrum object as required."""
   return (s if isinstance(s, ScriptableSpectrum) else ScriptableSpectrum(s))

def display(s):
   """display(s)
   Display a spectrum in the spectrum plot window.  This method takes care of converting internal spectra into ScriptableSpectra as necessary."""
   if isinstance(s, list):
      for ss in s:
          display(ss)
   else:
       DataManager.addSpectrum((s.getWrapped() if isinstance(s,ScriptableSpectrum) else s), True)
       
def clearSpectra():
   """Clear the spectrum display"""
   DataManager.clearSelections()

def report(html):
   """report(html)
   Append the specific syntactically correct HTML to the end of the report in the report tab."""
   MainFrame.appendHTML(html)

def mac(mat, xx, alg=epq.MassAbsorptionCoefficient.Chantler2005):
   """mac(mat, xx, [alg=epq.MassAbsorptionCoefficient.Chantler2005])
   where mat is a material or element (by name, Material or Element object), xx is an element, atomic shell or x-ray transition and alg is the tabulation to use (by default Chantler2005). Displays the mass absorption coefficient for the specified element or x-ray transition in the specified material."""
   mat = material(mat)
   if isinstance(xx, str):
       xx = element(xx)
   print "XRT\tMAC\tu(MAC)"
   print "\t(cm^2/g)\t(cm^2/g)"
   if isinstance(xx, epq.Element):
      for tr in range(epq.XRayTransition.KA1, epq.XRayTransition.N5N6 + 1):
         if epq.XRayTransition.exists(xx, tr):
            xrt = epq.XRayTransition(xx, tr)
            mm = alg.computeWithUncertaintyEstimate(mat, xrt)
            print "%s\t%g\t%g" % (xrt.toString(), alg.toCmSqrPerGram(mm.doubleValue()),alg.toCmSqrPerGram(mm.uncertainty()))
   elif isinstance(xx, epq.AtomicShell):
      for tr in range(epq.XRayTransition.getFirstIntoShell(xx), epq.XRayTransition.getLastIntoShell(xx)):
         if epq.XRayTransition.exists(xx, tr):
            xrt = epq.XRayTransition(xx, tr)
            mm = alg.computeWithUncertaintyEstimate(mat, xrt)
            print "%s\t%g\t%g" % (xrt.toString(), alg.toCmSqrPerGram(mm.doubleValue()),alg.toCmSqrPerGram(mm.uncertainty()))
   else:
      if isinstance(xx, epq.XRayTransition):
         xrt = xx
         mm = alg.computeWithUncertaintyEstimate(mat, xrt)
         print "%s\t%g\t%g" % (xrt.toString(), alg.toCmSqrPerGram(mm.doubleValue()),alg.toCmSqrPerGram(mm.uncertainty()))
      else:
         print xx

def getMac(elm, det=None, alg=epq.MassAbsorptionCoefficient.Chantler2005):
   """getMac(elm, [det=d1], [alg=epq.MassAbsorptionCoefficient.Chantler2005])
   Gets the mass absorption coefficient for the specified Element or Composition as a spectrum-like object. The det term (=d1) and the alg term (=epq.MassAbsorptionCoefficient.Chantler2005) are optional arguments."""
   if not det:
       det = findDetector("")
   elm = material(elm)
   if isinstance(det, epd.EDSDetector):
       chCount, chWidth, zeroOff = det.getChannelCount(), det.getChannelWidth(), det.getZeroOffset()
   else:
       chCount, chWidth, zeroOff = det, 10.0, 0.0
   macs = jarray.zeros(chCount, 'd')
   for i in range(0, chCount):
      e = chWidth * i + zeroOff
      if e > 0.0:
          macs[i] = alg.toCmSqrPerGram(alg.compute(elm, epq.ToSI.eV(e)))
   res = epq.SpectrumUtils.toSpectrum(chWidth, zeroOff, macs)
   epq.SpectrumUtils.renameSpectrum(res, "MAC[%s,%s]" % (elm, alg.getName()))
   return ScriptableSpectrum(res)

def displayMac(elm, eMax=20.48, alg=epq.MassAbsorptionCoefficient.Chantler2005):
   """displayMac(elm, eMax=20.48, alg=epq.MassAbsorptionCoefficient.Chantler2005)
   Displays the mass absorption coefficient for the specified Element or Composition in the spectrum display. The eMax term (=20.48) and the alg term (=epq.MassAbsorptionCoefficient.Chantler2005) are optional arguments."""
   display(getMac(elm, int(eMax / 0.01), alg))

def windowTransmission(name):
   """windowTransmission(name) or windowTransmission(window) or windowTransimission(detector)
   Creates a spectrum object representing the transmission of the window specified by name (see epd.XRayWindowFactory.WindowTypes for a list)."""
   if isinstance(name, str):
      w = epd.XRayWindowFactory.createWindow(name)
   elif isinstance(name, epd.EDSDetector):
      w = name.getWindow()
   elif isinstance(name, epd.IXRayWindowProperties):
      w = name
   if not isinstance(w, epd.IXRayWindowProperties):
      print "%s is not a window, detector or window name" % name
      return
   chCx = 4096
   chWidth = 10.0
   x = jarray.zeros(chCx, 'd')
   for ch in range(0, chCx):
      x[ch] = 100.0 * w.transmission(epq.ToSI.eV(ch * chWidth))
   res = wrap(epq.SpectrumUtils.toSpectrum(chWidth, 0, x))
   res.getProperties().setWindow(w)
   res.rename("Window[%s]" % (name))
   return res

def findDetector(name):
   """findDetector('Si(Li) at t=12us')
   Finds the first detector whose name starts with the specified string."""
   res = None
   if len(dets) > 0:
       res = dets[0]
   for det in dets:
      if det.toString().find(name) == 0:
         res = det
         break
   return res

def getTransitionSet(elm, family):
   """getTransitionSet('Fe','Ka')
   Returns an XRayTransitionSet object containing all the transitions associated with the specified transition family for the specified element where family is one of 'Ka', 'Kb', 'K', 'La', 'Lb', 'Lg', 'L*', 'L', 'Ma', 'Mb', 'Mg', 'M*', 'M'."""
   elm = element(elm)
   map = { "Ka" : epq.XRayTransitionSet.K_ALPHA,
           "Kb" : epq.XRayTransitionSet.K_BETA,
           "K"  : epq.XRayTransitionSet.K_FAMILY,
           "La" : epq.XRayTransitionSet.L_ALPHA,
           "Lb" : epq.XRayTransitionSet.L_BETA,
           "Lg" : epq.XRayTransitionSet.L_GAMMA,
           "L*" : epq.XRayTransitionSet.L_OTHER,
           "L" : epq.XRayTransitionSet.L_FAMILY,
           "Ma" : epq.XRayTransitionSet.M_ALPHA,
           "Mb" : epq.XRayTransitionSet.M_BETA,
           "Mg" : epq.XRayTransitionSet.M_GAMMA,
           "M*" : epq.XRayTransitionSet.M_OTHER,
           "M" : epq.XRayTransitionSet.M_FAMILY,
           "N" : epq.XRayTransitionSet.N_FAMILY }
   return epq.XRayTransitionSet(elm, map[family])

def textFile(filename):
   """textFile("output.txt")
   Create a text file using the java.io.PrintWriter class for writing to an UTF-8 file."""
   return jio.PrintWriter(filename, "UTF-8")

def ionizationRange(mat, e0=20.0, alg=epq.ElectronRange.KanayaAndOkayama1972):
   """ionizationRange(mat,[e0=20.0],[alg=epq.ElectronRange.KanayaAndOkayama1972])  Ex: ionizationRange(createMaterial(), 30.0)
      Tablulates the mean electron range for each element in the sample and each excitable shell."""
   mat = material(mat)
   print "   Material: %s" % mat
   print "Description: %s" % mat.descriptiveString(0)
   print "Beam energy: %g keV" % e0
   print "  Algorithm: %s" % alg.getName()
   print
   e = epq.ToSI.keV(e0)
   shells = [epq.AtomicShell.K, epq.AtomicShell.LIII, epq.AtomicShell.MV]
   if isinstance(mat, epq.Material):
      print "Shell\tRange"
      print "\t (&mu;m)"
   else:
      print "Shell\t Range"
      print "\t(&mu;m (g/cm^2))"
      mat = epq.Material(mat, epq.ToSI.gPerCC(1.0))
   for elm in mat.getElementSet():
      for shell in shells:
         sh = epq.AtomicShell(elm, shell)
         if sh.getEnergy() < e:
            print "%s\t%g" % (sh, alg.compute(mat, sh, e) / mat.getDensity()*1.0e6)


def filmThickness(film, substrate, e0, alg=epq.ElectronRange.KanayaAndOkayama1972):
   """filmThickness(film, substrate,e0,[alg=epq.ElectronRange.KanayaAndOkayama1972])  
   Computes how thick the film must be to sufficiently contain the electron beam such that \
none of the elements in substrate will be excited."""
   film = material(film)
   substrate = material(substrate)
   print "       Film: %s is %s" % (film, film.descriptiveString(0))
   print "  Substrate: %s is %s" % (substrate, substrate.descriptiveString(0))
   print "Beam energy: %g keV" % e0
   print "  Algorithm: %s" % alg.getName()
   print
   e = epq.ToSI.keV(e0)
   shells = [epq.AtomicShell.K, epq.AtomicShell.LIII, epq.AtomicShell.MV]
   if isinstance(film, epq.Material):
      print "Shell\tRange"
      print "\t (μm)"
   else:
      print "\t(μm (g/cm^2))"
      print "Shell\t Range"
      film = epq.Material(film, epq.ToSI.gPerCC(1.0))
   for elm in substrate.getElementSet():
      for shell in shells:
         sh = epq.AtomicShell(elm, shell)
         if sh.getEnergy() < e:
            print "%s\t%g" % (sh, alg.compute(film, sh, e) / film.getDensity()*1.0e6)


def readSpectra(filename, det=None):
    """readSpectra(filename)
    Example: res=readSpectra('/home/nicholas/spectra/k412.msa')
    Reads an array of spectra from a file on disk."""
    tmp = ept.SpectrumFile.open(filename)
    res = []
    for spec in tmp:
        if det:
            spec.getProperties().setDetector(det)
        res = res + [wrap(spec)]
    return res

def readSpectrum(filename, i=0, det=None):
    """readSpectrum(filename,i=0)
    Example: res=readSpectrum('/home/nicholas/spectra/k412.msa')
    Reads the i-th spectrum from a file on disk."""
    tmp = ept.SpectrumFile.open(filename)
    res = None
    if len(tmp) > i:
        res = wrap(tmp[i])
        if det:
            res.getProperties().setDetector(det)
    return res

def writeTextFile(filename, text):
    """writeTextFile()
    Writes text to a disk file."""
    f=file(filename,"w")
    try:
        f.write(text)
    finally:
        f.close()
    print "Text written to: %s" % filename


def readTextFile(filename):
    """readTextFile(filename)
    Read the contents of the specified file and return the result as a str."""
    f=open(filename,"r")
    try:
        res=f.read()
    finally:
        f.close()
    return res
        
def simulate(mat, det=None, keV=20.0, dose=60.0, withPoisson=True):
    '''simulate(mat,[det=d1],[keV=20.0],[dose=60.0],[withPoisson=True])
    Compute an analytical simulation of a spectrum for the specified \
bulk material with the specified detector, beam energy, dose (nA\267s).  \
If withPoisson then add count statistics otherwise the spectrum will \
contain fractional intensities and no simulated noise.  The material \
may be specified as a string (parsed with 'material(...)' or a \ 
Composition object'''
    if not det:
        det = findDetector("")
    mat = material(mat)
    sp = epq.SpectrumProperties(det.getProperties())
    sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy, keV)
    sp.setNumericProperty(epq.SpectrumProperties.FaradayBegin, 1.0)
    sp.setNumericProperty(epq.SpectrumProperties.LiveTime, dose)
    res = wrap(epq.SpectrumSimulator.Basic.generateSpectrum(mat, sp, det, True))
    if withPoisson:
        res = wrap(epq.SpectrumUtils.addNoiseToSpectrum(res, 1.0))
    res.rename("Simulated[%s,%0.1f keV,%0.2f nA\267s]" % (mat, keV, dose))
    return res

def mindat(comp, ira=True):
    '''mindat(comp)
    Look up the elements in comp in the mindat.org mineral database'''
    comp = material(comp)
    inc = ','.join(elm.toAbbrev() for elm in comp.getElementSet())
    exc = ','.join(elm.toAbbrev() for elm in epq.Element.allElements() if (comp.weightFraction(elm, 0) == 0.0) and (elm.getAtomicNumber() < 93))
    url = 'http://www.mindat.org/chemsearch.php?inc=%s&exc=%s%s&sub=Search+for+Minerals' % (inc, exc, ('&ima=0' if ira else ''))
    # print url
    bl().openURLinBrowser(url)

def mixture(matDict, density=0.0, name=None):
    '''mixture({ "U3O8" : 0.9, "ThO2" : 0.1 }, [density=9.0], [name='U+10%Th'])
    Creates a epq.Composition or epq.Material object representing \
the mass fraction weighed mixture of the specified list of materials. \
The materials may be epq.Composition/epq.Material objects or \
strings understood by material(...)'''
    res = epq.Composition()
    mats, qtys = [], []
    for mat, qty in matDict.items():
        mats.append(material(mat))
        qtys.append(qty)
    res.defineByMaterialFraction(mats, qtys)
    if density > 0:
        res = epq.Material(res, epq.ToSI.gPerCC(density))
    if not name:
        name = "Mixture[%s by mass]" % "+".join("%0.3f\267%s" % (qty, mat) for mat, qty in matDict.items())
    res.setName(name)
    return res

def compare(item, std=None):
   """compare(spec) or compare(comp1,comp2)
   1) Compares StandardComposition spectrum property to the MicroanalyticalComposition spectrum property.  Writes the result to the Report tab.
   2) Compares comp1 to comp2"""
   def sss(a):
      return reduce(lambda x, y: x + y, a, 0.0)
   if isinstance(item, epq.ISpectrumData) and (std == None):
      std = item.getProperties().getCompositionProperty(epq.SpectrumProperties.StandardComposition)
      mes = item.getProperties().getCompositionProperty(epq.SpectrumProperties.MicroanalyticalComposition)
      return compare(mes, std)
   absErr = dict(item.absoluteError(std, 0))
   relErr = dict(item.relativeError(std, 0))
   elms = absErr.keys()
   res = "<p><h3>Comparing Compositions</h3></p>\n"
   res = "%s<p>Comparing %s (measurement) to %s (standard)</p>\n" % (res, item, std)
   res = "%s<p><table align=\"center\">\n <tr><th>Element</th><th>Standard</th><th>Measured</th><th>Difference</th><th>%% Difference</th></tr>\n" % res
   for elm in absErr.keys():
      res = "%s<th>%s</th><td>%0.2f</td><td>%0.2f</td><td>%0.2f</td><td>%0.1f</td></tr>\n" % (res, elm.toAbbrev(), 100.0 * std.weightFraction(elm, 0), 100.0 * item.weightFraction(elm, 0), 100.0 * relErr.get(elm, 0.0), 100.0 * absErr.get(elm, 0.0))
   res = "%s<td>%d</td><td>%0.2f</td><td>%0.2f</td><td>%0.2f</td><td>%0.1f</td></tr>\n" % (res, len(elms), 100.0 * std.sumWeightFraction(), 100.0 * item.sumWeightFraction(), 100.0 * pow(sss(map(lambda a : a * a, relErr.values())), 0.5), 100.0 * pow(sss(map(lambda a: a * a, absErr.values())), 0.5))
   res = "%s</table></p>" % res
   report(res)
   
   
def quant(kratios, toa=40.0, e0=15.0, stds={}, elmByDiff=None, elmByStoic=None, assumedStoic={}, extraProps=None):
   """quant(kratios, toa = 40.0, e0 = 15.0, stds = {}, elmByDiff = None, elmByStoic = None, assumedStoic = {}, extraProps = None)
Performs a quantitative correction on the specified dictionary of kratios = { tr0 : kr}
+ kratios = { tr0 : kr0, tr1 : kr1, ..., trn : krn } where trX = epq.XRayTransition or epq.XRayTransition
  + XRayTransition can be constructed using 'transition(...)'
  + XRayTransitionSet can be constructed using 'getTransitionSet(elm, family)'
+ e0 - Beam energy in keV (or an IXRayDetector object)
+ toa - Take off angle in degrees
+ std = { elm0 : comp0, elm1 : comp1, ..., } where elmX is an element and compX is the associated composition
   + Missing elements are assumed to be pure
+ elmByDiff - Element to compute as a difference from 100%
+ elmByStoic - Element to compute using stoiciometry
+ assumedStoic = { elm0 : valence0, elm1 : valence1, ... } 
+ xtraProps - epq.SpectrumProperties() object with extra properties defined"""   
   sp = epq.SpectrumProperties()
   sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
   if isinstance(toa, epd.IXRayDetector):
      sp.addAll(toa.getProperties())
   else:
      sp.setNumericProperty(epq.SpectrumProperties.TakeOffAngle, toa)
   if extraProps:
      sp.addAll(extraProps)
   cfk = epq.CompositionFromKRatios()
   krs = epq.KRatioSet()
   pStds = {}
   for elm, std in stds.iteritems():
      pStds[element(elm)] = std
   for tr, kr in kratios.iteritems():
      if isinstance(tr, str):
         tr = transition(tr)
      elm = tr.getElement()
      std = (pStds[elm] if pStds.has_key(elm) else material(elm.toAbbrev(), 1.0))
      if not isinstance(tr, epq.XRayTransitionSet):
         tr = epq.XRayTransitionSet(tr)
      cfk.addStandard(tr, std, sp)
      krs.addKRatio(tr, kr)
   if isinstance(elmByDiff, epq.Element) or isinstance(elmByDiff, str):
      elmByDiff = element(elmByDiff)
      cfk.addUnmeasuredElementRule(epq.CompositionFromKRatios.ElementByDifference(elmByDiff))
   if (isinstance(elmByStoic, epq.Element) or isinstance(elmByStoic, str)) and (len(assumedStoic) > 1):
      elmByStoic = element(elmByStoic)
      pStoic = {}
      for elm, valence in assumedStoic.iteritems():
         pStoic[element(elm)] = valence
      uer = epq.CompositionFromKRatios.ElementByStoichiometry(elmByStoic, pStoic[elmByStoic], False)
      for elm, valence in pStoic.iteritems():
         if not elm.equals(elmByStoic):
            uer.add(elm, valence)
      cfk.addUnmeasuredElementRule(uer)
   return cfk.compute(krs, sp)

def multiQuant(det, e0, stds, refs={}, preferred=(), elmByDiff=None, elmByStoic=None, assumedStoic={}):
   """multiQuant(det, e0, stds, refs={}, preferred=(), elmByDiff = None, elmByStoic = None, assumedStoic = {})
Configure a QuantifyUsingStandards object which can be then used to quantifying multiple spectra.
Example:
    qus=multiQuant(det,e0,stds,refs)
    for spec in map:
        res=qus.compute(unknown)
        print res.getComposition()
       
+ det - The epq.EDSDetector
+ e0 - The beam energy in keV
+ stds - A dictionary mapping epq.Element into an ISpectrumData derived object
+ refs - (optional) A dictionary mapping an x-ray transition or x-ray transition set into an ISpectrumData object
+ preferred - (optional) A collection of XRayTransition objects specifying the preferred line for quantification
+ elmByDiff - (optional) Element to compute by difference from 100%
+ elmByStoic - (optional) Element to compute by assumed stoichiometry
+ assumedStoid - (optional, required if elmByStoic!=None) A dictionary mapping Element objects into the assumed valences"""

   qus = epq.QuantifySpectrumUsingStandards(det, epq.ToSI.keV(e0))
   for elm, spec in stds.iteritems():
      elm = element(elm)
      sp = spec.getProperties()
      sp.setDetector(det)
      comp = sp.getCompositionProperty(epq.SpectrumProperties.StandardComposition)
      qus.addStandard(elm, comp, spec)
   for xrt, spec in refs.iteritems():
      xrt = transition(xrt)
      elm = xrt.getElement()
      for roi in qus.getRegionOfInterestSet(elm):
         if roi.contains(xrt):
            qus.addReference(roi, spec)
   for xrt in preferred:
      xrt = transition(xrt)
      elm = xrt.getElement()
      for roi in qus.getRegionOfInterestSet(elm):
         if roi.contains(xrt):
            qus.setPreferredROI(elm, roi)
   if isinstance(elmByDiff, epq.Element) or isinstance(elmByDiff, str):
      elmByDiff = element(elmByDiff)
      qus.addUnmeasuredElementRule(epq.CompositionFromKRatios.ElementByDifference(elmByDiff))
   if (isinstance(elmByStoic, epq.Element) or isinstance(elmByStoic, str)) and (len(assumedStoic) > 1):
      elmByStoic = element(elmByStoic)
      pStoic = {}
      for elm, valence in assumedStoic.iteritems():
         pStoic[element(elm)] = valence
         uer = epq.CompositionFromKRatios.ElementByStoichiometry(elmByStoic, pStoic[elmByStoic], False)
      for elm, valence in pStoic.iteritems():
         if not elm.equals(elmByStoic):
            uer.add(elm, valence)
      qus.addUnmeasuredElementRule(uer)
   return qus   

def quantify(unknown, stds, refs={}, preferred=(), elmByDiff=None, elmByStoic=None, assumedStoic={}):
    """quantify(unk, stds, refs={}, preferred=(), elmByDiff = None, elmByStoic = None, assumedStoic = {})
    Quantify an unknown spectrum against a set of standard spectra.  You can optionally provide a set of \
references to use for shape information.  
+ unknown - An ISpectrumData derived object with EDSDetector defined
+ stds - A dictionary mapping epq.Element into an ISpectrumData derived object
+ refs - (optional) A dictionary mapping an x-ray transition or x-ray transition set into an ISpectrumData object
+ preferred - (optional) A collection of XRayTransition objects specifying the preferred line for quantification
+ elmByDiff - (optional) Element to compute by difference from 100%
+ elmByStoic - (optional) Element to compute by assumed stoichiometry
+ assumedStoid - (optional, required if elmByStoic!=None) A dictionary mapping Element objects into the assumed valences"""
    det = unknown.getProperties().getDetector()
    e0 = unknown.getProperties().getNumericProperty(epq.SpectrumProperties.BeamEnergy)
    qus = multiQuant(det, e0, stds, refs, preferred, elmByDiff, elmByStoic, assumedStoic)
    return qus.compute(unknown)
   
def electronRange(mat, e0, density=1.0):
    """electronRange(mat,e0, [density = 1.0])
    Computes the electron range (in meters) for the specified material at a beam energy of e0 keV.  The density is assumed to be 1.0 g/cm^3 \
unless density=None in which case the mat.getDensity() in g/cm^3 is used."""
    if isinstance(mat, str):
        mat = material(mat)
    if density == None:
        density = epq.FromSI.gPerCC(mat.getDensity())
    return epq.ElectronRange.KanayaAndOkayama1972.compute(mat, epq.ToSI.keV(e0)) / epq.ToSI.gPerCC(density)
 
def xrayRange(mat, e0, sh, density=1.0):
    """xrayRange(mat,e0, sh, [density = 1.0])
    Computes the x-ray excitation range (in meters) for the specified shell and material at a beam energy of e0 keV.  The density is assumed to be 1.0 g/cm^3 \
unless density=None in which case the mat.getDensity() in g/cm^3 is used."""
    if isinstance(sh, epq.XRayTransition):
       sh = sh.getDestination()
    return electronRange(mat, e0, density) - electronRange(mat, epq.FromSI.keV(sh.getEdgeEnergy()), density) 
 
 
def tabulate(specs, withErrs=False, normalize=False, prop=epq.SpectrumProperties.MicroanalyticalComposition, precision=4):
   """tabulate(specs,[withErrs=False],[normalize=False],[prop=epq.SpectrumProperties.MicroanalyticalComposition],[precision=4])
Tabulate the compositions associated with the specified collection of spectra.  Rows represent spectra and columns represent elements. \
You can use 'k', 'c' or 's' for prop for k-ratios, measured composition or standard composition respectively. precision>4 will output \
additional decimal digits of precision."""
   if isinstance(prop, str):
      propMap = { 
             'k' : epq.SpectrumProperties.KRatios,
             'c' : epq.SpectrumProperties.MicroanalyticalComposition,
             's' : epq.SpectrumProperties.StandardComposition
             }
      prop = propMap[prop]
   if prop <> epq.SpectrumProperties.KRatios:
      res = {}
      elms = ju.TreeSet()
      for spec in specs:
         c = spec.getProperties().getObjectWithDefault(prop, None)
         if c != None:
            res[spec] = c
            elms.addAll(c.getElementSet())
      tmp = "Name"
      stats = {}
      for elm in elms:
         tmp = "%s\t%s" % (tmp, elm.toAbbrev())
         if withErrs:
            tmp = "%s\td%s" % (tmp, elm.toAbbrev())
         stats[elm] = epu.DescriptiveStatistics()
      print tmp
      fmtStr="%s\t%2."+str(precision)+"f"
      for spec in res:
         c = res[spec]
         tmp = "%s" % spec
         for elm in elms:
            u = c.weightFractionU(elm, normalize)
            stats[elm].add(u.doubleValue())
            tmp = fmtStr % (tmp, 100 * u.doubleValue())
            if withErrs:
               tmp = fmtStr % (tmp, 100.0 * u.uncertainty())
         print tmp
      tmp = "Average"
      for elm in elms:
         tmp = fmtStr % (tmp, 100.0 * stats[elm].average())
         if withErrs:
            tmp = "%s\t" % tmp
      print tmp   
      tmp = "Std. Dev."
      for elm in elms:
         tmp = fmtStr % (tmp, 100.0 * stats[elm].standardDeviation())
         if withErrs:
            tmp = "%s\t" % tmp
      print tmp   
   else:
      res = {}
      xrtss = ju.TreeSet()
      for spec in specs:
         krs = spec.getProperties().getObjectWithDefault(prop, None)
         if krs != None:
            res[spec] = krs
            xrtss.addAll(krs.getTransitions())
      tmp = "Name"
      stats = {}
      for xrts in xrtss:
         stats[xrts] = epu.DescriptiveStatistics()
         tmp = "%s\t%s" % (tmp, xrts)
         if withErrs:
            tmp = "%s\td(%s)" % (tmp, xrts)
      print tmp
      fmtStr="%s\t%2."+str(precision)+"f"
      for spec in res:
         k = res[spec]
         tmp = "%s" % spec
         for xrts in xrtss:
            u = k.getKRatioU(xrts)
            stats[xrts].add(u.doubleValue())
            tmp = fmtStr % (tmp, u.doubleValue())
            if withErrs:
               tmp = fmtStr % (tmp, u.uncertainty())
         print tmp
      tmp = "Average"
      for xrts in xrtss:
         tmp = fmtStr % (tmp, stats[xrts].average())
         if withErrs:
            tmp = "%s\t" % tmp
      print tmp   
      tmp = "Std. Dev."
      for xrts in xrtss:
         tmp = fmtStr % (tmp, stats[xrts].standardDeviation())
         if withErrs:
            tmp = "%s\t" % tmp
      print tmp   
      
def phirhoz(comp, det, e0, nSteps=100, alg=epq.XPP1991()):
   """phirhoz(comp, det, e0, nSteps=100, alg=epq.XPP1991())
   Computes the raw and absorbed phi(rhoz) curves for the specified composition material \
   at the specified beam energy and detected by the specified detector.""" 
   comp = material(comp)
   sp = epq.SpectrumProperties(det.getProperties())
   sp.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
   xrts = majorTransitions(comp, e0)
   rhoZmax = epq.ElectronRange.KanayaAndOkayama1972.compute(comp, epq.ToSI.keV(e0))
   print "Material\t%s" % comp
   print "Beam energy\t%g keV" % e0
   print "Algorithm\t%s" % alg.getName()
   print "Detector\t%s" % det
   print "Take-off\t%g%s" % (jl.Math.toDegrees(epq.SpectrumUtils.getTakeOffAngle(det.getProperties())), epq.SpectrumProperties.TakeOffAngle.getUnits())
   res = "Idx\trhoz"
   for xrt in xrts:
      res = "%s\tG(%s)\tE(%s)" % (res, xrt, xrt)
   print res      
   print "\t(mg/cm^2)"
   for step in range(0, nSteps):
      rz = step * rhoZmax / nSteps
      res = "%d\t%g" % (step, 100.0 * rz) # in mg/cm^2
      for xrt in xrts:
         alg.initialize(comp, xrt.getDestination(), sp)
         res = "%s\t%g\t%g" % (res, alg.computeCurve(rz), alg.computeAbsorbedCurve(xrt, rz))
      print res         
      
def annotComposition(prop=epq.SpectrumProperties.MicroanalyticalComposition):
   """annotComposition(prop=epq.SpectrumProperties.MicroanalyticalComposition)
   Annotate the spectrum display window with the composition of the selected \
   spectrum or average of the selected spectra."""
   ss = selected()
   if len(ss) == 1:
      comp = ss[0].getProperties().getCompositionProperty(prop)
      res = "Element\tWgt Frac\tAtom Frac"
      for elm in comp.getElementSet():
         res = "%s\n%s\t%0.4f\t%0.4f" % (res, elm.toAbbrev(), comp.weightFraction(elm, False), comp.atomicPercent(elm))
      res = "%s\nTotal\t%0.4f\t%0.4f" % (res, comp.sumWeightFraction(), 1.0)
   else:
      dsm = {}
      for s in ss:
         comp = s.getProperties().getCompositionProperty(prop)
         for elm in comp.getElementSet():
            if not dsm.has_key(elm):
               dsm[elm] = epu.DescriptiveStatistics()
      for s in ss:
         comp = s.getProperties().getCompositionProperty(prop)
         for elm, ds in dsm.iteritems():
            ds.add(comp.weightFraction(elm, False))
      res = "Average composition\nElement\tWgt Fract\tStdDev"
      for elm, ds in dsm.iteritems():
         res = "%s\n%s\t%0.4f\t%0.4f" % (res, elm.toAbbrev(), ds.average(), ds.standardDeviation())
   MainFrame.setSpectrumText(res);
   
def setAnnotation(ss):
   """setAnnotation("An annotation\twith tabs\nnew lines and other goodies.")
   Underlay a text annotation on the spectrum display window."""
   MainFrame.setSpectrumText(ss) 
         
def clearAnnotation():
   """clearAnnotation()
   Clears all annotations on the spectrum display window."""
   MainFrame.setSpectrumText(None)
   
def dump(spec, positiveOnly=True):
   """dump(spec,positiveOnly=True)
   Dumps the raw spectrum data to the command window in a two column format."""
   eVperCh = spec.getChannelWidth()
   off = spec.getZeroOffset()
   end = spec.getChannelCount()
   for ch in range(spec.getChannelCount() - 1, 0, - 1):
      if spec.getCounts(ch) != 0.0:
         end = ch + 1;
         break;
   st = (epq.SpectrumUtils.channelForEnergy(spec, 0.0) if positiveOnly else 0)
   print "Energy\tIntensity"
   print "(eV)\t(Counts)"
   for ch in range(st, end):
      print "%g\t%g" % (off + eVperCh * ch, spec.getCounts(ch))
      
def selectedRegions():
   """selectedRegions()
   Returns a list of the ranges of energies as selected on the spectrum display."""
   regs = MainFrame.spectrumDisplay.getRegions()
   res = []
   for r in (regs.get(i) for i in range(0, regs.size())):
      res.append((r.getLowEnergy(), r.getHighEnergy()))
   return res

def selectedChannels(det):
   """selectedChannels()
   Returns a list of the ranges of channels as selected on the spectrum display."""   
   regs = MainFrame.spectrumDisplay.getRegions()
   res = []
   for r in (regs.get(i) for i in range(0, regs.size())):
      res.append((det.channelForEnergy(r.getLowEnergy()), det.channelForEnergy(r.getHighEnergy())))
   return res
         
def countEvents(specs, dose=False):
   """countEvents(specs)
   Computes the background corrected peak integral for the spectra in specs using the regions \
   highlighted on the spectrum display and reports the results in tabular form.""" 
   if isinstance(specs, epq.ISpectrumData):
         specs = (specs,)
   regs = MainFrame.spectrumDisplay.getRegions()
   tmp = ""
   for r in (regs.get(i) for i in range(0, regs.size())):
      tmp = "%s\t%1.1f eV\t%1.1f eV\t\t" % (tmp, r.getLowEnergy(), r.getHighEnergy())
   print tmp
   tmp = "Spectrum"
   for r in (regs.get(i) for i in range(0, regs.size())):
      tmp = "%s\tPeak\tErr\tTotal\tBkg" % tmp
   print tmp
   for spec in specs:
      sp = spec.getProperties()
      dd = (sp.getNumericWithDefault(epq.SpectrumProperties.LiveTime, 1.0e100) * epq.SpectrumUtils.getAverageFaradayCurrent(sp, 1.0e100) if dose else 1.0)
      tmp = "%s" % spec
      for r in (regs.get(i) for i in range(0, regs.size())):
         bci = epq.SpectrumUtils.backgroundCorrectedIntegral(spec, r.getLowEnergy(), r.getHighEnergy() - 1.0e-8)
         err, sum, bkg = bci[1], bci[2], bci[3]
         tmp = "%s\t%1.1f\t%1.1f\t%1.1f\t%1.1f" % (tmp, (sum - bkg) / dd, err / dd, sum / dd, bkg / dd)
      print tmp

def dumpComps(comps):
   """dumpComps(comps)
   Outputs a collection of compositions (as weight fraction) in a table."""
   all = set()
   for comp in comps:
      all = all | set(comp.getElementSet())
   tmp = "Material"
   for elm in all:
      tmp = "%s\t%s" % (tmp, elm.toAbbrev())
   print tmp
   for comp in comps:
      tmp = str(comp)
      for elm in all:
         tmp = "%s\t%6.4f" % (tmp, comp.weightFraction(elm, False))
      print tmp

def listMaterials():
   """listMaterials()
   Outputs a list containing all items in the standard composition database."""
   return map(material, Database.getStandards().keySet()) 
      
def sum(specs, newname=None, std=None):
    """sum(specs,newname=None,std=None)
    Returns the channel-by-channel sum of a list of spectra. Sets the name to newname and \
    the standard composition to material(std)."""
    res = wrap(reduce(ScriptableSpectrum.__add__, (wrap(spec) for spec in specs)))
    for spec in specs:
       ts = spec.getProperties().getTimestampWithDefault(epq.SpectrumProperties.AcquisitionTime, None)
       if ts:
          res.getProperties().setTimestampProperty(epq.SpectrumProperties.AcquisitionTime, ts)
          break
    res.rename((newname if newname else "Sum"))
    if std:
       res.getProperties().setCompositionProperty(epq.SpectrumProperties.StandardComposition, material(std))
       if newname == None:
          res.rename("%s std" % std)
    return res

def bcPeakIntegral(spec, det=None, comp=None):
   """bcPeakIntegral(spec,[det=None],[comp=None])
   Computes the background correctd peak integral for the range of channels selected \
   on the spectrum display.  If det and comp are specified in the spectrum these \
   need not be specified as arguments."""
   sp = spec.getProperties()
   if det == None:
      det = sp.getDetector()
   if comp == None:
      comp = epq.SpectrumUtils.getComposition(spec)
   bkg = wrap(epq.BremsstrahlungAnalytic.DTSA.fitBackground(det, spec, comp))
   sc = selectedChannels(det)
   lrb, lrs = epu.LinearRegression(), epu.LinearRegression(),
   for r in selectedChannels(det):
      for ch in range(r[0], r[1] + 1):
         lrs.addDatum(ch, spec.getCounts(ch))
         lrb.addDatum(ch, bkg.getCounts(ch))
   # print lrs
   # print lrb
   r0, r1 = selectedChannels(det)
   minCh, maxCh, avgCh = r0[1], r1[0], 0.5 * (r0[1] + r1[0])
   # print "%g\t%g" % ( lrs.computeY(avgCh), lrb.computeY(avgCh))
   bkg = (lrs.computeY(avgCh) / lrb.computeY(avgCh)) * bkg
   delta = wrap(spec) - bkg
   dose = epq.SpectrumUtils.getAverageFaradayCurrent(sp, 1.0e100) * sp.getNumericProperty(epq.SpectrumProperties.LiveTime)
   return epq.SpectrumUtils.backgroundCorrectedIntegral(delta, r0[1], r1[0], r0[0], r0[1], r1[0], r1[1])[0] / dose

def backscatter(comp, e0=20.0):
   """backscatter(comp,e0)
   Estimates the backscatter coefficient for the specified \
   composition at the specified beam energy (keV)"""
   if isinstance(comp, epq.Element):
      comp = epq.Composition([comp], [1.0])
   return epq.BackscatterCoefficient.Love1978.compute(material(comp), epq.ToSI.keV(e0))
 
 
def zafU(unk, det, e0, stds = {}, trs = ( epq.XRayTransition.KA1, epq.XRayTransition.LA1, epq.XRayTransition.MA1 )):
    """zafU(unk, det, e0, stds = {}, trs = ( epq.XRayTransition.KA1, epq.XRayTransition.LA1, epq.XRayTransition.MA1 ))
    zafU calculates the ZAF correction along with an estimate of the uncertainty for the specified unknown material, \
using the specified standards and detector."""
    unk = material(unk)
    elms = unk.getElementSet()
    if not trs:
        trs = epq.XRayTransition.ALL_TRANSITIONS
    props = epq.SpectrumProperties()
    props.addAll(det.getProperties())
    props.setNumericProperty(epq.SpectrumProperties.BeamEnergy, e0)
    print "XRT\tStd\tMACstd\tU(MACstd)\tMACunk\tU(MACunk)\tC\tdC\tdC/C (%)"
    for elm in elms:
        abbrev=elm.toAbbrev()
        if stds.has_key(abbrev):
            std=material(stds[abbrev])
        else:
            if defaultStandards.has_key(abbrev):
                std=material(defaultStandards[abbrev])
            else:
                std=material(abbrev)
        mac = epq.XPP1991().getAlgorithm(epq.MassAbsorptionCoefficient);
        for tr in trs:
            if epq.XRayTransition.exists(elm,tr) and (epq.XRayTransition.getEnergy(elm,tr)<0.9*epq.ToSI.keV(e0)):
                xrt=epq.XRayTransition(elm,tr)
                cc = epq.XPP1991().massFraction(std, unk, xrt, props)
                macS = mac.computeWithUncertaintyEstimate(std, xrt)
                macU = mac.computeWithUncertaintyEstimate(unk, xrt)
                print "%s\t%s\t%4.4f\t%4.4f\t%4.4f\t%4.4f\t%4.4f\t%4.4f\t%2.2f"  % ( xrt, std, macS.doubleValue(), macS.uncertainty(), macU.doubleValue(), macU.uncertainty(), cc.doubleValue(), cc.uncertainty(), cc.fractionalUncertainty()*100)
 
 
def isTerminated():
   return terminated

def init_dets(globs):
   """Used internally to initialize the detector variables d1, d2, ..."""
   di=Database.getDetectorsInt()
   tmp=[]
   for ep in Database.getCurrentProbes():
      for det in Database.getCurrentEDSDetectors(ep):
         dp=det.getDetectorProperties()
         if dp in di:
            ii=di[dp]
            globs['d%d' % ii]=det
            tmp.append(det)
   globs['dets']=tmp
   
def findStandards(elm, min=0.1, max=1.0, sim=False):
    """findStandards(elm, min=0.1, max=1.0, simulate=False):
    Search the standard database for suitable materials for use as a standard for the specified element."""
    elm=element(elm)
    sdb=App.getStandardsDatabase()
    stds=sdb.findStandards(elm, min)
    for std in stds:
        if std.weightFraction(elm,False)<=max:
            print std.descriptiveString(False)
            print "\tAvailable: %s" % ", ".join(("'%s'" % str(std) for std in sdb.find(std.getName())))
            if sim:
                display(simulate(std,d1,keV=25.0))

def describe(x):
    """describe(x) 
    Writes a text description of the material 'x'"""
    x=material(x)
    print x
    print "Element\tZ\tMass Frac\tNorm Mass\tAtom Frac"
    for elm in x.getElementSet():    
        print "%s\t%d\t%g\t%g\t%g" % (elm, elm.atomicNumber, x.weightFraction(elm,False), x.weightFraction(elm,True), x.atomicPercent(elm))
    print "--\t%g\t%g\t1.0\t1.0" % (x.meanAtomicNumber(), x.sumWeightFraction())

def installPlugIn(name, func):
    """Install a plug-in with a menu item in the the action of which is define by the function 'func'"""
    MainFrame.installPlugIn(name, func)

def exit():
    '''exit()
    Close the DTSA-II application.'''
    MainFrame.fileExit()
	
_xxx_=init_dets(globals())
del _xxx_