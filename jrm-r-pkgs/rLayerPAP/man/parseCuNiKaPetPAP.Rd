\name{parseCuNiKaPetPAP}
\alias{parseCuNiKaPetPAP}
\title{Parse a GMRFilm PAP simulation for Cu on Ni on PET}
\usage{
  parseCuNiKaPetPAP(v.kv, kr.file.path)
}
\arguments{
  \item{v.kv}{A vector with the simuted acellerationg
  voltages \code{v.kv}}

  \item{kr.file.path}{file path to the K-Ratio file
  \code{kr.file.path}}
}
\value{
  df A data frame with the e0, krNiKa, krCuKa
}
\description{
  This reads in a vector of the acellerating voltages
  simulated and the the file containing the K-ratios for Ni
  K-alpha and Cu K-alpha lines and returns a data frame
  with the values. These are input to optimization
  routines.
}
\examples{
R code here showing how your function works
}
\keyword{keywords}

