\name{print.capability}
\alias{print.capability}
\title{Print method for class capability }
\description{
\code{print.capability} implements generic print method for class capability. Summary variable statistics and overall capability indexes are printed out.
}
\usage{
\method{print}{capability}(x,\dots)
}

\arguments{
  \item{x}{ an object of class capability}
\item{...}{further arguments to be added}
}
\details{
NA value is returned for any index not computed.
}
\value{
No values are returned}
\references{ Bothe (1997), Measuring Process Capability, McGraw Hill}
\author{ Giorgio Spedicato }
\note{ Output returned is a coincise version of \code{\link{summary.capability}} output.
}
\seealso{ \code{\link{summary.capability}}}
\examples{
data(brakeCap)
x=brakeCap$quencing
sg=brakeCap$subgroup
capObj=capabilityNormal(x=x,sg=sg, lsl=41,usl=42, target=41.5, name="example data")
print.capability(capObj)
}
\keyword{ methods }

