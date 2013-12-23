\name{parseNiCuOut}
\alias{parseNiCuOut}
\title{Parse a GMRFilm PAP simulation for Ni on Cu on PET}
\usage{
parseNiCuOut(fPath)
}
\arguments{
  \item{fPath}{File path to the K-Ratio file \code{fPath}}
}
\value{
df A data frame with the e0, krNiKa, krCuKa
}
\description{
This reads an output file (fPath) produced by GMRFilm using
writeInputNiCuSG containing Ni K-alpha and Cu K-alpha
K-ratios for specified values of Ni and Cu thickness and a
vector of accelerating voltages and returns a data frame
with the values. These are input to optimization routines.
}
\examples{
### not run
# wrkDir <- "C:/Temp/"
# vkV <- 10:30
# setwd(wrkDir)
# preClean(wrkDir)
# makeRunIt(wrkDir)
# inFil <- './in.txt'
# writeInputNiCuSG(200, 400, vkV, inFil)
# system("runIt", show.output.on.console=TRUE)
# kFil  <- getOutputFile()
# df <- parsePdCuOut(kFil)
# print(df)
}
\keyword{keywords}

