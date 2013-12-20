\name{write.gmrf.in.pd.cu}
\alias{write.gmrf.in.pd.cu}
\title{Write an input file for a StrataGem type simulation for CuPd}
\usage{
write.gmrf.in.pd.cu(t.pd, t.cu, v.kv, fpath, toa = 35)
}
\arguments{
  \item{t.pd}{Thickness of Pd in nm \code{t.pd}}

  \item{t.cu}{Thickness of Cu in nm \code{t.pd}}

  \item{v.kv}{A vector of voltages to simulate \code{v.kv}}

  \item{fpath}{full path to the output file (input for
  GMRFilm) \code{fPath}}

  \item{toa}{The detector take-off angle, \code{v.kv}}
}
\value{
none No return value but writes the specified output
}
\description{
Write an input file for GMRFilm to construct an input file
for GMRFilm to compute the K-ratios for Pd La and Cu Ka for
a vector of accelerating voltages and specified thickness
values by any spaces.
}
\examples{
### not run
}
\keyword{keywords}

