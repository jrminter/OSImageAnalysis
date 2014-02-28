\name{parseCuOxOut}
\alias{parseCuOxOut}
\title{Parse a GMRFilm PAP simulation for CuOx on Cu}
\usage{
parseCuOxOut(fPath)
}
\arguments{
  \item{fPath}{File path to the K-Ratio file \code{fPath}}
}
\value{
ret A vector with the e0, tOx, krOKa, krCuLa
}
\description{
This reads an output file (fPath) produced by GMRFilm using
writeInputCuOxCu containing O K-alpha and Cu L-alpha
K-ratios for a single thickness thickness and e0
}
\examples{
### not run
# wrkDir <- "C:/Temp/"
# e0 = 5
# setwd(wrkDir)
# preClean(wrkDir)
# makeRunIt(wrkDir)
# inFil <- './in.txt'
# writeInputCuOxCu.R(50.0, 0.1386, 0.8614, 3.0, 5.0, inFil, toa=35)
# system("runIt", show.output.on.console=TRUE)
# kFil  <- getOutputFile()
# res <- parseCuOxOut(kFil)
# print(res)
}
\keyword{keywords}

