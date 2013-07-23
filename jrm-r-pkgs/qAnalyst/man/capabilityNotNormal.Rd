\name{capabilityNotNormal}
\alias{capabilityNotNormal}
\title{ Capability object creator for non - normal data}
\description{
 \code{capabilityNotNormal} function creates capability class object for non - normal data given specification limits. \code{plot}, \code{print}, \code{summary} methods are avaible for capability class objects.
}
\usage{
capabilityNotNormal(x,  lsl = NULL, usl = NULL, target = NULL, distribution,
    name = deparse(substitute(x)),  toler=6, histPars=c(NA,NA))
}
\arguments{
  \item{x}{ a numeric data vector.}
  \item{lsl}{ lower specification limit.}
  \item{usl}{ upper specification limit.}
  \item{target}{ process target.}
  \item{distribution}{ distribution of the variable.}
  \item{name}{ name of the variable, default taken by "x" name. }
  \item{toler}{width of tolerance specification. Default is 6, that is six sigma.}
  \item{histPars}{a vector of two elements that allows user to specify historical mean and standard deviation respectively.}
}
\details{
  Either lsl or usl must be specified. Hypothized distribution must be specified. \code{capabilityNotNormal} is a wrapper of many internal functions, that check user specifications consistency and perform calculation of statistics. Results are stored in a capability object.
}
\value{ A capability object list is returned }
\references{ Bothe (1997), Measuring Process Capability, McGraw Hill }
\author{ Giorgio Spedicato }
\note{ Creates the core capability objects}
\seealso{ \code{\link{plot.capability}}, \code{\link{print.capability}}, \code{\link{summary.capability}} }
\examples{
data(warpTiles)
capObj=capabilityNotNormal(x=warpTiles$warping, usl=8, target=40, distribution="weibull",
    name="warping")
summary(capObj)
  }
\keyword{ methods }
