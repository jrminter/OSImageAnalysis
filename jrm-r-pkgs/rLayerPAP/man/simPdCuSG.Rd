\name{simPdCuSG}
\alias{simPdCuSG}
\title{Compute PAP K-Ratios for Pd/Cu using GMRFilm}
\usage{
simPdCuSG(vkV, tPd, tCu, toa, wrkDir = "C:/Temp/", clean = FALSE)
}
\arguments{
  \item{vkV}{A vector of kvs to simulate}

  \item{tPd}{Pd thickness in nm}

  \item{tCu}{Cu thickness in nm}

  \item{toa}{take off angle for detector in deg}

  \item{wrkDir}{Working directory}

  \item{clean}{Boolean to delete input/output files}
}
\value{
df A data frame with the kVs and the Pd and Cu K-a K-ratios
}
\description{
Compute the PdKa and CuKa K-ratios using GMRFilm for a
vector of accelerating voltages for specified Pd and Cu
thickness values. Note: this corrects for continuum
fluorescence
}
\examples{
### Not run
# vkV <- 10:30
# print(vkV)
# df <- simPdCuSG(vkV, 8.8, 861., 35.0, wrkDir='C:/Temp/', clean=FALSE)
# print(head(df))
}
\keyword{keywords}

