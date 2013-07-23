\name{plot.transformation}
\alias{plot.transformation}
\title{ plot method for class transformation }
\description{
\code{plot.transformation} implements generic plot method for transformation class objects. Plot of transformation objects is performed by trellis graphics.}
\usage{
\method{plot}{transformation}(x, \dots)
}

\arguments{
  \item{x}{ an object of class transformation. }
  \item{\dots}{ further arguments to be added. }
}
\details{
 \code{plot.transformation} makes use of trellis function histograms. Two histograms are plotted onto the same graph. Leftward the original data distribution is plotted. Rightward the trasformed data distribution is plotted.
}
\value{
No values are returned}
\references{ Lattice package help manual }
\author{ Giorgio Spedicato }
\note{ Generic S3 function method
}
\seealso{ \code{\link{johnsonFun}}, \code{\link{boxcoxFun}} }
\examples{
#warpTiles data set
data(warpTiles)
johnsonWarp=johnsonFun(warpTiles$warping)
plot(johnsonWarp)
}

\keyword{ methods }
