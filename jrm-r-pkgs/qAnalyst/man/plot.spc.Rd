\name{plot.spc}
\alias{plot.spc}
\title{Plot method for spc class objects}
\description{\code{plot.spc} implements generic plot method for spc class objects.  Plot of spc object is performed by trellis graphics.
}
\usage{
\method{plot}{spc}(x,cex = list(cexStrip=2, cexAxes=2, cexScales=2,cexPoints=1.5), \dots)
}
\arguments{
\item{x}{ An object of class spc}
\item{cex}{ A list containing cex parameter for Strip, Axes, Scales and Points}
\item{...}{furter arguments to be added}
}
\details{\code{plot.spc} requires lattice library.}
\value{No value is returned}
\references{ Lattice package help manual }
\author{Andrea Spano' }
\note{ An spc object is required}
\seealso{  \code{\link{spc}}, \code{\link{print}} }
\examples{
#brakeCap
data(brakeCap)
x=brakeCap$hardness
sg=brakeCap$subgroup
go=spc(x=x,sg=sg,type="xbar")
plot(go)
}
\keyword{ methods }

