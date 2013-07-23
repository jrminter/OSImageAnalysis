\name{plot.capability}
\alias{plot.capability}
\title{ Plot method for class capability}
\description{
\code{plot.capability} implements generic plot method for capability class objects. Plot of capability objects is performed by trellis graphics.
}
\usage{
\method{plot}{capability}(x, \dots)
}
\arguments{
  \item{x}{ an object of class capability.}
 \item{...}{further arguments to be added}
}
\details{
\code{plot.capability} makes use of trellis function histogram.
}
\value{
This function return no value.}
\references{ Lattice package help manual }
\author{ Giorgio Spedicato }
\note{ Generic S3 function method
}
\seealso{  \code{\link{capability}}}
\examples{
#creates capability obj
data(brakeCap)
capObj=capabilityNormal(x=brakeCap$hardness, sg=brakeCap$subgroup, usl=41.5)
plot.capability(capObj)
}
\keyword{ methods }

