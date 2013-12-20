\name{parseCuPdLaPetPAP}
\alias{parseCuPdLaPetPAP}
\title{Parse a GMRFilm PAP simulation for Pd on Pd on PET}
\usage{
parseCuPdLaPetPAP(v.kv, kr.file.path)
}
\arguments{
  \item{v.kv}{A vector with the simulated accelerating
  voltages \code{v.kv}}

  \item{kr.file.path}{file path to the K-Ratio file
  \code{kr.file.path}}
}
\value{
df A data frame with the e0, krPdLa, krCuKa
}
\description{
This reads in a vector of the accelerating voltages
simulated and the the file containing the K-ratios for Pd
L-alpha and Cu K-alpha lines and returns a data frame with
the values. These are input to optimization routines.
}
\examples{
### not run
}
\keyword{keywords}

