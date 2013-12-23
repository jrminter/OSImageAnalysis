\name{pap.sim.ni.cu}
\alias{pap.sim.ni.cu}
\title{Compute PAP K-Ratios for Ni/Cu using GMRFilm}
\usage{
pap.sim.ni.cu(v.kv, t.ni, t.cu, toa, wrkDir = "C:/Temp/", clean = FALSE)
}
\arguments{
  \item{v.kv}{A vector of kvs to simulate \code{v.kv}}

  \item{t.ni}{Ni thickness in nm \code{t.ni}}

  \item{t.cu}{Cu thickness in nm \code{t.cu}}

  \item{toa}{take off angle for detector in deg \code{toa}}

  \item{wrkDir}{Working directory \code{wrkDir}}

  \item{clean}{Boolean to delete input/output
  files\code{clean}}
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
# v.kV <- 10:30
# print(v.kV)
# df <- pap.sim.ni.cu(v.kV, 8.8, 861., 35.0, wrkDir='C:/Temp/', clean=FALSE)
# print(head(df))
}
\keyword{keywords}

