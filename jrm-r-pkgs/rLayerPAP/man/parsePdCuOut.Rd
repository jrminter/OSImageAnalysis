\name{parsePdCuOut}
\alias{parsePdCuOut}
\title{Parse a GMRFilm PAP simulation for Pd on Cu on PET}
\usage{
  parsePdCuOut(fPath)
}
\arguments{
  \item{fPath}{File path to the K-Ratio file}
}
\value{
  df A data frame with the e0, krPdLa, krCuKa
}
\description{
  This reads an output file (fPath) produced by GMRFilm
  using writeInputPdCuSG containing Pd L-alpha and Cu
  K-alpha K-ratios for specified values of Pd and Cu
  thickness and a vector of accelerating voltages and
  returns a data frame with the values.
}
\details{
  These are input to optimization routines.
}
\examples{
### not run
# wrkDir <- "C:/Temp/"
# vkV <- 10:30
# setwd(wrkDir)
# preClean(wrkDir)
# makeRunIt(wrkDir)
# inFil <- './in.txt'
# writeInputPdCuSG(200, 400, vkV, inFil)
# system("runIt", show.output.on.console=TRUE)
# kFil  <- getOutputFile()
# df <- parsePdCuOut(kFil)
# print(df)
}
\keyword{keywords}

