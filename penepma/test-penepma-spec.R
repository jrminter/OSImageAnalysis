# Plot a penenepma spectrum from the penepma dir
# A helper function to analyze penepma runs on-the-fly
# and plot the final spectrum when finished
#
# 2018-07-22 requires the rpenepma package from github
#
#
# set paths and kV

library(here)
print(here())

print(getwd())

gitDir <- Sys.getenv('GIT_HOME')
relDir <- "OSImageAnalysis/penepma"
spcTi  <- "Ir-500-on-Ag-250-on-Silica-30kV-jw"
outTi  <- "Ir-500-on-Ag-250-on-Silica-jwa"
penPa  <- "C:/UserData/Penepma12/Penepma"
e0     <-   30.0 # kV
doMsa  <- FALSE # Usually only want to write the final one...
pWid   <- 1024
pHt    <-  768
ptSz   <-   12

# should not need to change below here...

library(rpenepma)

inFil <- sprintf("%s/%s", penPa, "pe-spect-01.dat" )

outFil <- sprintf("%s/%s/%s.msa", gitDir, relDir, spcTi )

df <- penepma_read_raw_data(inFil)
rownames(df) <- c()
print(head(df))
print(summary(df))


plt <- penepma_plot_spectrum(inFil, spcTi)
print(plt)


outPng <- sprintf("%s/%s/%s-linear.png", gitDir, relDir, spcTi )

png(outPng, width = pWid, height = pHt, units = "px")

plt <- plt + theme(axis.text=element_text(size=24),
                   axis.title=element_text(size=24),
                   plot.title = element_text(size=28, hjust = 0.5)) +
  # coord_trans(y= "sqrt") +
  NULL
print(plt)
dev.off()


plt <- penepma_plot_spectrum_logy(inFil, spcTi)
print(plt)

outPng <- sprintf("%s/%s/%s-logY.png", gitDir, relDir, spcTi )


png(outPng, width = pWid, height = pHt, units = "px")
plt <- plt + theme(axis.text=element_text(size=24),
                   axis.title=element_text(size=24),
                   plot.title = element_text(size=28, hjust = 0.5)) +
  # coord_trans(y= "sqrt") +
  NULL
print(plt)
dev.off()


if (doMsa == TRUE) {
  outFil <- sprintf("%s/%s/%s.msa", gitDir, relDir, outTi )
  penepma_to_msa(inFil, outFil, e0, outTi)
}

