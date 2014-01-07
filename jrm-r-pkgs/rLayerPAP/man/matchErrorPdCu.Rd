\name{matchErrorPdCu}
\alias{matchErrorPdCu}
\title{Generate the K-Ratio match error for Pd on Cu using a PAP model}
\usage{
  matchErrorPdCu(vkV, vPdKR, vCuKR, vPdTh, vCuTh, waitSec,
    wrkDir = "C:/Temp/")
}
\arguments{
  \item{vkV}{A vector of accelerating voltages (kV) to
  simulate}

  \item{vPdKR}{A vector of PdLa K-ratios measured at vkV}

  \item{vCuKR}{A vector of CuKa K-ratios measured at vkV}

  \item{vPdTh}{A vector of Pd thickness values (nm) to
  simulate}

  \item{vCuTh}{A vector of Cu thickness (nm) to simulate}

  \item{waitSec}{time to wait for OS to rename output file}

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
# vkV   <- c(10, 12, 15, 20, 25, 30)
# vPdKR <- c(0.14713, 0.11593, 0.08533, 0.04546, 0.03498, 0.02327)
# vCuKR <- c(0.55999, 0.75381, 0.80997, 0.85107, 0.78985, 0.66039)
# vPdTh <- seq(from=5.0, to=30.0, by=5.0)
# vCuTh <- seq(from=810.0, to=860.0, by=5.0)
# df <- matchErrorPdCu(vkV, vPdKR, vCuKR, vPdTh, vCuTh, 0.1,  wrkDir="C:/Temp/")
}
\keyword{keywords}

