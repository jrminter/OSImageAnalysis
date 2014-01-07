\name{matchErrorNiCu}
\alias{matchErrorNiCu}
\title{Generate the K-Ratio match error for Ni on Cu using a PAP model}
\usage{
  matchErrorNiCu(vkV, vNiKR, vCuKR, vNiTh, vCuTh, waitSec,
    wrkDir = "C:/Temp/")
}
\arguments{
  \item{vkV}{A vector of accelerating voltages (kV) to
  simulate}

  \item{vNiKR}{A vector of NiLa K-ratios measured at vkV}

  \item{vCuKR}{A vector of CuKa K-ratios measured at vkV}

  \item{vNiTh}{A vector of Ni thickness values (nm) to
  simulate}

  \item{vCuTh}{A vector of Cu thickness (nm) to simulate}

  \item{waitSec}{time to wait for OS to rename output file}

  \item{wrkDir}{A working directory for the computation}
}
\value{
  A data frame with t.Ni, t.Cu, and rms.dev
}
\description{
  Use GMRFilm to compute the RMS deviation between
  experimental Ni K-alpha and Cu K-alpha K-Ratios and model
  values computed using the Phi-Rho-Z model of Pouchou and
  Pichoir (1991).
}
\examples{
### Not run
# qm-03692-DJ2-d1
# vkV   <- c(12, 15, 20, 25, 30)
# vNiKR <- c(0.0741, 0.0628, 0.0257, 0.0188, 0.0117)
# vCuKR <- c(0.9004, 0.8847, 0.7693, 0.5739, 0.4045)
# vNiTh <- seq(from=5.0, to=30.0, by=5.0)
# vCuTh <- seq(from=500.0, to=550.0, by=5.0)
# df <- matchErrorNiCu(vkV, vNiKR, vCuKR, vNiTh, vCuTh, 0.1,  wrkDir="C:/Temp/")
}
\keyword{keywords}

