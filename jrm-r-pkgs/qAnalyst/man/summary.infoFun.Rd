\name{summary.infoFun}
\alias{summary.infoFun}
\title{ Generic summary method for infoFun objects }
\description{\code{summary.infoFun} implements generic summary method on infoFun objects. Estimated parameters names and values are print out, with AD statistics if calculated}
\usage{
\method{summary}{infoFun}(object, \dots)
}
\arguments{
  \item{object}{ An object of class infoFun }
  \item{...}{ furter arguments to be added }
}
\details{
\code{summary.infoFun} output is build from infoFun objects internal list items.
}
\value{
No values are returned}
\references{No refrences}
\author{ Giorgio Spedicato }
\note{No notes }
\seealso{  \code{\link{funInfoFun}}}
\examples{
#warpTiles data
data(warpTiles)
infoX=funInfoFun(warpTiles$warping, "weibull")
summary(infoX)
}
\keyword{ methods }
