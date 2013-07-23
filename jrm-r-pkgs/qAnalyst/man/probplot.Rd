\name{probplot}
\alias{probplot}
\title{ Function to plot probability plots }
\description{
\code{probplot} plots probability plot for a vector of values, given distribution specifications. Confidence intervals and a legend can be plot too.
}
\usage{
probplot(x, distribution, theta, confintervals = FALSE,
    confidence = 0.95,  name = deparse(substitute(x)))
}
\arguments{
  \item{x}{ a vector of values. }
  \item{distribution}{ character specifying distribution to plot }
  \item{theta}{vector of parameter. Estimated by the function if left missing}
  \item{confintervals}{ logical item, indicating wherether confidence interval have to be plotted or not. }
  \item{confidence}{ confidence \eqn{1-\alpha} level. }
  \item{name}{ name of variable plotted. }
}
\details{
(x,y) values represent respectively original data and corresponding quantiles of theorethical estimated distribution. If the theoretical distribution fits data well, values should lies around the straight line plotted.
}
\value{
\code{probplot} returns no value}
\references{No references}
\author{ Giorgio Spedicato }
\note{No notes }
\seealso{  \code{\link{funInfoFun}}}
\examples{
data(warpTiles)

probplot(x=warpTiles$warping,distribution="weibull", confintervals=TRUE,
    confidence=.95,  name="warping")
}
\keyword{ methods }

