\name{print.transformation}
\alias{print.transformation}
\title{ Print method for class capability  }
\description{
\code{print.transformation} implements generic print method for class transformation. Type of performed transformation and estimated parameters are printed out.}
\usage{
\method{print}{transformation}(x, \dots)
}
\arguments{
  \item{x}{ an object of class transformation }
  \item{...}{ further arguments to be added }
}
\details{No details}
\value{
No values are returned}
\references{No references }
\author{ Andrea Spano'}
\note{No notes}
\seealso{  \code{\link{boxcoxFun}}, \code{\link{johnsonFun}}, \code{\link{plot.transformation}} }
\examples{
data(warpTiles)
boxcoxWarp=boxcoxFun(warpTiles$warping)
print(boxcoxWarp)
}
\keyword{ methods }
