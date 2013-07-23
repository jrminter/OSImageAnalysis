\name{andersonDarlingFun}
\alias{andersonDarlingFun}
\title{ Function to obtain Anderson Darling statistics and p-value }
\description{
\code{andersonDarlingFun} returns a vector containing AD test statistics and corresponding p-value, from given data and distribution specification.
}
\usage{
andersonDarlingFun(x, distribution, theta)
}
\arguments{
  \item{x}{ a vector of data }
  \item{distribution}{ character string specifying hypothized distribution }
  \item{theta}{vector of parameter, coherent with \code{distribution} specification}
}
\details{
\code{andersonDarlingFun} currently supports following distributions: normal, lognormal, gamma, weibull, logistic.
}
\value{
A vector of two elements: statistics and p-value}
\references{ Stephens, M.A., eds.: Goodness-of-Fit Techniques. Marcel Dekker, New York. }
\author{ Andrea Spano', Enrico Pegoraro, Giorgio Spedicato }
\note{No notes}
\seealso{  \code{\link{funInfoFun}}}
\examples{
data(warpTiles)
x=warpTiles$warping
infoX=funInfoFun(x,"weibull")
andersonDarlingFun(x=x, infoX$densfun, infoX$theta)
}
\keyword{ methods }

