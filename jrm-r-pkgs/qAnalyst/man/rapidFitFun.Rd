\name{rapidFitFun}
\alias{rapidFitFun}
\title{ Function to obtain rapid fitting of multiple distributions }
\description{
\code{rapidFitFun} fits parameter on data vector x for some of most important continuous distributions.
Fitted parameters values and names are printed out in a table together. Anderson Darling goodness of fit statistics p-value is moreover provided.
}
\usage{
rapidFitFun(x, rounding = 3, boxcox=FALSE, johnson=FALSE)
}
\arguments{
  \item{x}{ a vector of countinuous values. All values must be positive }
  \item{rounding}{ rounding digits to obtain pretty table printing }
  \item{boxcox}{Boolean. If true, boxcox normality transformation is performed}
  \item{johnson}{Boolean. If true, johnson normality transformation is performed}
}
\details{
\code{rapidFitFun} uses \code{funInfoFun} functionalities to estimate parameters and AD p-value. If either boxcox or johnson are TRUE, estimated AD statistics p-value is related to trasformed data.
}
\value{
\code{rapidFitFun} returns no value
}
\references{ Graybill Mood, Introduction to Statistics, Mc-Graw Hill }
\author{ Giorgio Spedicato }
\note{ \code{rapidFitFun} is a wrapper for \code{funInfoFun}. Numerical procedures to obtain parameters MLE may not always converge.
In such cases warnings and errors message may be thrown. 
}
\seealso{ \code{\link{funInfoFun}}, \code{\link{andersonDarlingFun}}}
\examples{
##brakeCap
data(brakeCap)
rapidFitFun(brakeCap$centering)
#warptiles
data(warpTiles)
rapidFitFun(warpTiles$warping)
}
\keyword{ methods}
