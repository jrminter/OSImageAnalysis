\name{write.gmrf.in.ni.cu}
\alias{write.gmrf.in.ni.cu}
\title{Write an input file for a StrataGem type simulation for CuNi}
\usage{
write.gmrf.in.ni.cu(t.ni, t.cu, v.kV, fpath, toa = 35)
}
\arguments{
  \item{t.ni}{Thickness of Ni in nm \code{t.ni}}

  \item{t.cu}{Thickness of Cu in nm \code{t.cu}}

  \item{v.kV}{a vector of voltage (kV) to simulate
  \code{v.kV}}

  \item{fpath}{full path to the output file (input for
  GMRFilm) \code{fPath}}

  \item{toa}{The detector take-off angle, \code{toa}}
}
\value{
none No return value but writes the specified output
}
\description{
Write an input file for GMRFilm to construct an input file
for GMRFilm to compute the K-ratios for Ni Ka and Cu Ka for
a specified thickness of Ni and Cu for a vector of kV
values.
}
\examples{
### not run
#
# setwd("C:/Temp/")
# v.kV = c(10, 12, 15, 20, 25, 30)
# write.gmrf.in.ni.cu(200, 400, v.kV, './in.txt')
}
\keyword{keywords}

