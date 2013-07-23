\name{devFun}
\alias{devFun}
\title{ Internal function to estimate deviance}
\description{
\code{devFun} computes the sum of square deviations from a center. devFun is used to estimate deviance or if a target is specified cpm statistic.
}
\usage{
devFun(x, center = "mean")
}

\arguments{
  \item{x}{ data vector }
  \item{center}{ a numeric value or "mean" (default) to estimate usual deviance statistic}
}
\details{
Internal function
}
\value{
A numeric value of the deviance estimation}
\references{ Internal function }
\author{ Giorgio Spedicato }
\note{ Internal function
}
\seealso{  \code{\link{capabilityNormal}}}
\examples{
x=c(2,3,4,5,6)
devFun(x)
}
\keyword{ methods }
\keyword{ internal }
