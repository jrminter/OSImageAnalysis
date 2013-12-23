\name{parse.pd.cu.gmrf.sg.out}
\alias{parse.pd.cu.gmrf.sg.out}
\title{Parse a GMRFilm PAP simulation for Pd on Cu on PET}
\usage{
parse.pd.cu.gmrf.sg.out(gmrf.sg.path)
}
\arguments{
  \item{gmrf.sg.path}{File path to the K-Ratio file
  \code{gmrf.sg.path}}
}
\value{
df A data frame with the e0, krPdLa, krCuKa
}
\description{
This reads an output file (gmrf.sg.path) produced by
GMRFilm using write.gmrf.in.pd.cu containing Pd L-alpha and
Cu K-alpha K-ratios for specified values of Pd and Cu
thickness and a vector of accelrating voltages and returns
a data frame with the values.
}
\details{
These are input to optimization routines.
}
\examples{
### not run
# setwd("C:/Apps/GMRFilm/")
# df <- parse.pd.cu.gmrf.sg.out("./out-PdCu.txt")
#print(df)
}
\keyword{keywords}

