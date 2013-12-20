\name{pap.sim.pd.cu}
\alias{pap.sim.pd.cu}
\title{Compute PAP K-Ratios for Pd/Cu using GMRFilm}
\usage{
pap.sim.pd.cu(v.kv, t.pd, t.cu, toa, pgDir = "C:/Apps/GMRfilm",
  clean = TRUE)
}
\arguments{
  \item{v.kv}{A vector of kvs to simulate \code{v.kv}}

  \item{t.pd}{Pd thickness in nm \code{t.pd}}

  \item{t.cu}{Cu thickness in nm \code{t.cu}}

  \item{toa}{take off angle for detector in deg \code{toa}}

  \item{pgDir}{location of GMRFilm \code{pgDir}}

  \item{clean}{Boolean to delete input/output
  files\code{clean}}
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
}
\keyword{keywords}

