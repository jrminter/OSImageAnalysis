\name{writeInputNiCuSG}
\alias{writeInputNiCuSG}
\title{Write an input file for a StrataGem type simulation for CuNi}
\usage{
  writeInputNiCuSG(tNi, tCu, vkV, fPath, toa = 35)
}
\arguments{
  \item{tNi}{Thickness of Ni in nm \code{tNi}}

  \item{tCu}{Thickness of Cu in nm \code{tCu}}

  \item{vkV}{A vector of voltage to simulate \code{vkV}}

  \item{fPath}{full path to the output file \code{fPath}}

  \item{toa}{The detector take-off angle \code{toa}}
}
\value{
  none
}
\description{
  Write an input file for GMRFilm to construct an input
  file for GMRFilm to compute the K-ratios for Ni Ka and Cu
  Ka for a specified thickness of Ni and Cu for a vector of
  kV values.
}
\examples{
### not run
}
\keyword{keywords}

