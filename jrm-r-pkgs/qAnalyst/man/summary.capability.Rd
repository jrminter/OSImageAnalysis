\name{summary.capability}
\alias{summary.capability}
\title{Summary method for class capability}
\description{
\code{summary.capability} implements generic summary method for capability class objects. A thorough report of performed analysis results is printed out. Three sections are printed: summary variables statistics, estimated ppm, capability index.
}
\usage{
\method{summary}{capability}(object, printPotential = TRUE, printOverall = TRUE, printPerc = FALSE,
    printZeta = FALSE, \dots)
}
\arguments{
  \item{object}{ an object of capability obj }
  \item{printPotential}{ ask use if potential stastistics shall be printed, default true. }
  \item{printOverall}{ ask use if overall stastistics shall be printed, default true.}
  \item{printPerc}{ ask uses if percentages have to be used in place of ppm, default false. }
  \item{printZeta}{ ask uses if zeta values have to be used in place of capability statistics, default false. }
  \item{\dots}{ further arguments to be added }
}
\details{
\code{summary.capability} expands \code{print.capability} output.
}
\value{
No value is returned}
\references{ Bothe (1997), Measuring Process Capability, McGraw Hill }
\author{ Giorgio Spedicato }
\note{ This function is an S3 primitive
}
\seealso{ \code{\link{print.capability}}}
\examples{
data(brakeCap)
x=brakeCap$hardness
sg=brakeCap$subgroup
capObj=capabilityNormal(x=x, sg=sg, lsl=39, usl=41, target=40, name="example data")
summary.capability(capObj)
}
\keyword{ methods }
