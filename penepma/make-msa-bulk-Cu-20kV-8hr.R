library(rEDS)

gitDir <- Sys.getenv('GIT_HOME')
relDir <- "OSImageAnalysis/penepma"


inFil <- sprintf("%s/%s/%s", gitDir, relDir,
                 "bulk-Cu-20kV-8hr-sim.dat" )

outFil <- sprintf("%s/%s/%s", gitDir, relDir,
                  "bulk-Cu-20kV-8hr-sim.msa" )

penepmaToMsa(inFil, outFil, 20.0, "bulk-Cu-20kV-8hr-sim")
