library(rEDS)

gitDir <- Sys.getenv('GIT_HOME')
relDir <- "OSImageAnalysis/penepma"


inFil <- sprintf("%s/%s/%s", gitDir, relDir,
                 "pe-spect-01.dat" )

outFil <- sprintf("%s/%s/%s", gitDir, relDir,
                  "pe-spect-01.msa" )

df <- penepma_read_raw_data(inFil)
rownames(df) <- c()
print(head(df))
print(summary(df))


plt <- penepma_plot_spectrum(inFil, "pe-spect-01")
print(plt)

plt <- penepma_plot_spectrum_logy(inFil, "pe-spect-01")
print(plt)

# penepmaToMsa(inFil, outFil, 20.0, "pe-spect-01")
