\name{writeInputNiCuTh}
\alias{writeInputNiCuTh}
\title{Write an input file to simulate of a range Ni thickness on Cu}
\usage{
  writeInputNiCuTh(vNi, tCu, e0, fPath, toa = 35)
}
\arguments{
  \item{vNi}{A vector of thickness of Ni in nm \code{vNi}}

  \item{tCu}{Thickness of Cu in nm \code{tCu}}

  \item{e0}{A voltage (kV) to simulate \code{e0}}

  \item{fPath}{full path to the output file \code{fPath}}

  \item{toa}{The detector take-off angle \code{toa}}
}
\value{
  none
}
\description{
  Write an input file for GMRFilm to construct an input
  file for GMRFilm to compute the K-ratios for Ni Ka and Cu
  Ka for a vector of Ni thickness (nm) a at a single Cu
  thickness (tCu) and kV (e0).
}
\examples{
### not run
}
\keyword{keywords}

