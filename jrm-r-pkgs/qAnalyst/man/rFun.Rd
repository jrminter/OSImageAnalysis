\name{rFun}
\alias{rFun}
\title{ Internal function to compute range values}
\description{
 \code{rFun} returns the absolute value of the range of a data vector: (max - min).
}
\usage{
rFun(x)
}
\arguments{
  \item{x}{data vector.}
}
\details{
x may contain NA values.
}
\value{
The range numeric value is returned. It may be NA if all elements in input data are NA.
}
\references{ Internal function }
\author{ Andrea Spano' and Giorgio Spedicato }
\note{ \code{rFun} is mainly an internal function used by various other routines.
}
\seealso{  \code{\link{centerFun}}, \code{\link{clFun}} }
\examples{
#1 example
x=c(1,2,3,NA, NA)
print(rFun(x))
# 2 example
x=c(NA,NA,NA,NA, NA)
print(rFun(x))
}
\keyword{ methods }
\keyword{ internal }
