\name{warpTiles}
\alias{warpTiles}
\docType{data}
\title{ Warp tiles dataframe}
\description{
WarpTiles dataframe contains measurement about warp in a tiles factory.
}
\usage{data(warpTiles)}
\format{
  A data frame with 100 observations on the following variable.
  \describe{
    \item{\code{warping}}{a numeric vector}
  }
}
\details{
Tiles distribution is well fitted by a Weibull or a Gamma distribution.
}
\source{
Industrial data.
}
\references{
warpTiles dataframe may be used to show capability for non - normal data.
}
\examples{
data(warpTiles)
plot(capabilityNotNormal(x=warpTiles$warping, usl=8, distribution="weibull", name="WARP"))
}
\keyword{datasets}
