\name{xLimitsFun}
\alias{xLimitsFun}

\title{ Internal function to return x variable confidence limits plotting coordinates}
\description{\code{xLimitsFun} receives a x vector and returns a sorted vector of length 2*length(x) with duplicated x elements.}
\usage{xLimitsFun(x)}

\arguments{
  \item{x}{ a vector.}
}
\details{\code{xLimitsFun} is an internal function defined to plot confidence limits. Therefore x is a vector of integer representing x coordinates of points.}
\value{The object returned is a vector of coordinates.}
\references{ Internal function }
\author{ Andrea Spano' }
\note{ Used by spc}
\seealso{  \code{\link{spc}}}
\examples{
#only for illustrative purpuoses
x=c(1,2,3,4)
output=xLimitsFun(x)
# 1 1 2 2 3 3 4 4
}
\keyword{ methods }
\keyword{ internal }
