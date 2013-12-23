\name{parse.ni.cu.gmrf.sg.out}
\alias{parse.ni.cu.gmrf.sg.out}
\title{Parse a GMRFilm PAP simulation for Ni on Cu on PET}
\usage{
parse.ni.cu.gmrf.sg.out(gmrf.sg.path)
}
\arguments{
  \item{gmrf.sg.path}{File path to the K-Ratio file
  \code{gmrf.sg.path}}
}
\value{
df A data frame with the e0, krNiKa, krCuKa
}
\description{
This reads an output file (gmrf.sg.path) produced by
GMRFilm using write.gmrf.in.ni.cu containing Ni K-alpha and
Cu K-alpha K-ratios for specified values of Ni and Cu
thickness and a vector of accelrating voltages and returns
a data frame with the values. These are input to
optimization routines.
}
\examples{
### not run
# setwd("C:/Temp/")
# df <- parse.ni.cu.gmrf.sg.out("./out.txt")
# print(df)
}
\keyword{keywords}

