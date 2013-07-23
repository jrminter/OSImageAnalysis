\name{countFun}
\alias{countFun}
\title{ Internal function to count the number of non missing values }
\description{\code{countFun} counts the number of non missing values in a vector.
}
\usage{countFun(x)}
\arguments{
  \item{x}{ data vector }
}
\details{
Internal function.
}
\value{
an integer whose value is the number of non - missing values.
}
\references{ Internal function }
\author{ Andrea Spano' and Giorgio Spedicato }
\note{ countFun is an internal function used by centerFun and stats4CapFun}
\seealso{ \code{\link{centerFun}}}
\examples{
## Simple example
a=c(NA,NA,2,4,6,1,NA)
countFun(a)
#4}
\keyword{ internal }
\keyword{ methods }
