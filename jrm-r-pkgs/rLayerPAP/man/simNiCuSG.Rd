\name{simNiCuSG}
\alias{simNiCuSG}
\title{Compute PAP K-Ratios for Ni/Cu using GMRFilm}
\usage{
simNiCuSG(vkV, tNi, tCu, toa, wrkDir = "C:/Temp/", clean = FALSE)
}
\arguments{
  \item{vkV}{A vector of kvs to simulate}

  \item{tNi}{Ni thickness in nm}

  \item{tCu}{Cu thickness in nm}

  \item{toa}{take off angle for detector in deg}

  \item{wrkDir}{Working directory}

  \item{clean}{Boolean to delete input/output files}
}
\value{
df A data frame with the kVs and the Ni and Cu K-a K-ratios
}
\description{
Compute the NiKa and CuKa K-ratios using GMRFilm for a
vector of accelerating voltages for specified Ni and Cu
thickness values. Note: this corrects for continuum
fluorescence
}
\examples{
### Not run
}
\keyword{keywords}

