\name{write.gmrf.in.ni.th.cu}
\alias{write.gmrf.in.ni.th.cu}
\title{Write an input file for a simulation of a range Ni thickness on Cu}
\usage{
write.gmrf.in.ni.th.cu(v.ni, t.cu, e0, fpath, toa = 35)
}
\arguments{
  \item{v.ni}{A vector of thickness of Ni in nm
  \code{v.ni}}

  \item{t.cu}{Thickness of Cu in nm \code{t.cu}}

  \item{e0}{A voltage (kV) to simulate \code{e0}}

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
a vector of Ni thickness (nm) a at a single Cu thickness
(tCu)
}
\examples{
### not run
#
# setwd("C:/Temp/GMRFilm/")
# v.ni = c(50, 100, 200)
# write.gmrf.in.ni.th.cu(v.ni, 400, 15, './in.txt')
}
\keyword{keywords}

