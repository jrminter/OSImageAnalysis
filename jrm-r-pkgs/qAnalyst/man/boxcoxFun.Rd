\name{boxcoxFun}
\alias{boxcoxFun}
\title{Function to obtain Box Cox transformations}
\description{
\code{boxcoxFun} performs box cox transformation, finding optimal lambda for the given data vector. \code{boxcoxFun} returns a transformation class object.
}
\usage{
boxcoxFun(x)
}
\arguments{
  \item{x}{ numeric data vector }
}
\details{
\code{boxcoxFun} calls internally \code{powerTransform} and \code{bcPower1} functions from package car to build output transformation object.
}
\value{
 A transformation class object is returned. A transformation class objects consists in a list composed by the following items:
  \item{type}{type of transformation, in such case: "boxcox"}
  \item{parameters}{parameter lambda is stored in this item}
  \item{original}{original data vector}
  \item{parameters}{trasformed data vector}
}
\references{Venables, Ripley Modern Applied Statistics with S-PLUS}
\author{Giorgio Spedicato, Nicola Sturaro Sommacal}
\note{Box cox transformations requires data to be positive. X vector positivity is internally checked before performing transformation.}
\seealso{\code{\link{print.transformation}}, \code{\link{plot.transformation}}, \code{\link{johnsonFun}} }
\examples{
#warpTiles example
data(warpTiles)
boxInfo=boxcoxFun(x=warpTiles$warping)
print(boxInfo)
}
\keyword{ methods }
