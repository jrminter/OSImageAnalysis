# Plot a penepma spectrum and optionally convert to .msa format
# 2018-07-20 requires the rpenepma package from github
#
#
# set paths and kV

gitDir <- Sys.getenv('GIT_HOME')
relDir <- "OSImageAnalysis/penepma"
spcTi  <- "pe-spect-01"
e0     <- 30.0 # kV
doMsa  <- FALSE # Usually only want to write the final one...

# shold not need to change below here...

library(rpenepma)

inFil <- sprintf("%s/%s/%s", gitDir, relDir, "pe-spect-01.dat" )

outFil <- sprintf("%s/%s/%s.msa", gitDir, relDir, spcTi )

df <- penepma_read_raw_data(inFil)
rownames(df) <- c()
print(head(df))
print(summary(df))


plt <- penepma_plot_spectrum(inFil, spcTi)
plt <- plt +
       # coord_trans(y= "sqrt") +
       NULL
print(plt)

plt <- penepma_plot_spectrum_logy(inFil, spcTi)
print(plt)

if (doMsa == TRUE) {
  penepma_to_msa(inFil, outFil, e0, spcTi)
}

