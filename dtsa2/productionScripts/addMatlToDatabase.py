import gov.nist.microanalysis.EPQLibrary as epq
import dtsa2.jmGen as jmg
import os, shutil

gitDir  = os.environ['GIT_HOME']
relPrj  = "/OSImageAnalysis/dtsa2/productionScripts/"
prjDir  = gitDir + relPrj
rptDir  = prjDir + '/addMatlToDatabase Results/'


kapton = epq.Material(epq.Composition([ epq.Element.C,
                                            epq.Element.O,
                                            epq.Element.N,
                                            epq.Element.H],
                                           [ 0.69113,
                                             0.20924,
                                             0.07327,
                                             0.02636 ]
                                          ),
                                          epq.ToSI.gPerCC(1.420))

jmg.addMatToDatabase(kapton, "Kapton", 1.4200)


# clean up cruft
shutil.rmtree(rptDir)
print "Done!"
