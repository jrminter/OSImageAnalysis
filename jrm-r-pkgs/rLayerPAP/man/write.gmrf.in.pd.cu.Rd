\name{write.gmrf.in.pd.cu}
\alias{write.gmrf.in.pd.cu}
\title{Write an input file for a StrataGem type simulation for CuPd}
\usage{
write.gmrf.in.pd.cu(v.pd, t.cu, e0, fpath, toa = 35)

write.gmrf.in.pd.cu(v.pd, t.cu, e0, fpath, toa = 35)
}
\arguments{
  \item{t.pd}{Thickness of Pd in nm \code{t.pd}}

  \item{t.cu}{Thickness of Cu in nm \code{t.cu}}

  \item{v.kV}{a vector of voltage (kV) to simulate
  \code{v.kV}}

  \item{fpath}{full path to the output file (input for
  GMRFilm) \code{fPath}}

  \item{toa}{The detector take-off angle, \code{toa}}

  \item{v.pd}{A vector of thickness of Pd in nm
  \code{v.pd}}

  \item{t.cu}{Thickness of Cu in nm \code{t.cu}}

  \item{e0}{A voltage (kV) to simulate \code{e0}}

  \item{fpath}{full path to the output file (input for
  GMRFilm) \code{fPath}}

  \item{toa}{The detector take-off angle, \code{toa}}
}
\value{
none No return value but writes the specified output

none No return value but writes the specified output
}
\description{
Write an input file for GMRFilm to construct an input file
for GMRFilm to compute the K-ratios for Pd Ka and Cu Ka for
a specified thickness of Pd and Cu for a vector of kV
values.

Write an input file for GMRFilm to construct an input file
for GMRFilm to compute the K-ratios for Pd La and Cu Ka for
a vector of accelerating voltages and specified thickness
values by any spaces.
}
\examples{
### not run
#
# setwd("C:/Apps/GMRFilm/")
# v.kV = c(10, 12, 15, 20, 25, 30)
# write.gmrf.in.pd.cu(200, 400, v.kV, './in.txt')
### not run
#
# setwd("C:/Temp/GMRFilm/")
# v.pd = c(50, 100, 200)
# write.gmrf.in.pd.cu(v.pd, 400, 15, './in.txt')
}
\keyword{keywords}

