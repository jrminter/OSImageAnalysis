\name{getCoeffFun}
\alias{getCoeffFun}
\title{ Internal wrapper function to getParameterFun }
\description{
\code{getCoeffFun} returns the parameters from Montgomery book A6 coefficients table. Coefficients from A6 table are used in control charts construction.
}
\usage{
getCoeffFun(sampleSize, coeff)
}

\arguments{
  \item{sampleSize}{ A vector of subgroups size. }
  \item{coeff}{ a string that specifies the required parameters. }
}
\details{Internal function}
\value{
A vector of coefficients.
}
\references{ Montgomery, Statistical Quality Control }
\author{ Giorgio Spedicato and Andrea Spano'}
\note{ getCoeffFun is a wrapper for \code{getParameter}. getCoeffFun handles missing values, returning NA if subgroup dimension is NA.
}
\seealso{ \code{\link{getParameterFun}}}
\examples{
##Simple example
sgDim=c(10,5,8,10)
getCoeffFun(sgDim,"d3")
# 0.797 0.864 0.820 0.797
}
\keyword{ internal }
\keyword{ methods}
