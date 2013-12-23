\name{matchErrorPdCu}
\alias{matchErrorPdCu}
\title{Generate the K-Ratio match error for Pd on Cu using a PAP model}
\usage{
matchErrorPdCu(vkV, vPdKR, vCuKR, PdLo, PdHi, PdSt, CuLo, CuHi, CuSt,
  wrkDir = "C:/Temp/")
}
\arguments{
  \item{vkV}{A vector of accelerating voltages (kV) to
  simulate}

  \item{vPdKR}{A vector of PdLa K-ratios measured at vkV}

  \item{vCuKR}{A vector of CuKa K-ratios measured at vkV}

  \item{PdLo}{lowest Pd thickness values (nm) to simulate}

  \item{PdHi}{highest Pd thickness values (nm) to simulate}

  \item{PdSt}{Pd thickness step (nm)}

  \item{CuLo}{lowest Cu thickness (nm) to simulate}

  \item{CuHi}{highest Cu thickness (nm) to simulate}

  \item{CuSt}{Cu thickness (nm) step}

  \item{wrkDir}{A working directory for the computation}
}
\value{
A data frame with t.Pd, t.Cu, and rms.dev
}
\description{
Use GMRFilm to compute the RMS deviation between
experimental Pd L-alpha and Cu K-alpha K-Ratios and model
values computed using the Phi-Rho-Z model of Pouchou and
Pichoir (1991).
}
\examples{
### Not run
}
\keyword{keywords}

