\name{write.gmrf.in.ni.cu}
\alias{write.gmrf.in.ni.cu}
\title{Write an input file for a StrataGem type simulation for CuNi}
\usage{
  write.gmrf.in.ni.cu(t.ni, t.cu, v.kv, fpath, toa = 35)
}
\arguments{
  \item{t.ni}{Thickness of Ni in nm \code{t.ni}}

  \item{t.cu}{Thickness of Cu in nm \code{t.ni}}

  \item{v.kv}{A vector of voltages to simulate \code{v.kv}}

  \item{fpath}{full path to the output file (input for
  GMRFilm) \code{fPath}}

  \item{toa}{The detector take-off angle, \code{v.kv}}
}
\value{
  none No return value but writes the specified output
}
\description{
  Write an input file for GMRFilm to construct an input
  file for GMRFilm to compute the K-ratios for Ni Ka and Cu
  Ka for a vector of acellerating voltages and specifed
  thickeness values by any spaces.
}
\examples{
### not run
}
\keyword{keywords}

