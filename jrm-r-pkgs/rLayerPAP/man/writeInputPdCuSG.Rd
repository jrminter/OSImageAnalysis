\name{writeInputPdCuSG}
\alias{writeInputPdCuSG}
\title{Write an input file for a StrataGem type simulation for CuPd}
\usage{
  writeInputPdCuSG(tPd, tCu, vkV, fPath, toa = 35)
}
\arguments{
  \item{tPd}{Thickness of Pd in nm}

  \item{tCu}{Thickness of Cu in nm}

  \item{vkV}{A vector of voltage to simulate}

  \item{fPath}{Path to the output file}

  \item{toa}{The detector take-off angle}
}
\value{
  none
}
\description{
  Write an input file for GMRFilm to construct an input
  file for GMRFilm to compute the K-ratios for Pd Ka and Cu
  Ka for a specified thickness of Pd and Cu for a vector of
  kV values.
}
\examples{
### not run
}
\keyword{keywords}

