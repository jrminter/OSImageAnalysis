\name{c4Fun}
\alias{c4Fun}
\title{ Internal function to estimate unbiasing correction constant for standard deviation }
\description{
\code{c4Fun} function returns the unbiasing costant used to correct sample standard deviation estimation.
}
\usage{
c4Fun(x)
}

\arguments{
  \item{x}{ Sample dimension }
}
\details{
  Data are supposed to be normally distributed.
}
\value{ a numeric value of the unbiasing constant}
\references{ Bothe (1997), Measuring Process Capability, McGraw Hill }
\author{ Giorgio Spedicato }
\note{ This is an internal function
}
\seealso{  \code{\link{capabilityNormal}} }
\examples{
c4Fun(c(2,3,4,5))
}
\keyword{ methods }
\keyword{ internal }
