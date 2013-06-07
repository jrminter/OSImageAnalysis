\name{normal.bin}
\alias{normal.bin}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{
A function to bin data and compute parameters for a single mode normal distribution
}
\description{
Computes equally-spaced logarithmic bins from a vector and computes the parameters for a single mode normal distribution.
}
\usage{
normal.bin(x, do.plot = FALSE, nBreaks = 10)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
A vector of observations
}
  \item{do.plot}{
A Boolean - determines whether the histogram is plotted
}
  \item{nBreaks}{
The number of bins
}
}
\details{
%%  ~~ If necessary, more details than the description above ~~
}
\value{
A list containing
  \item{data }{a data frame with x (bin midpoint), cts (counts), dens (histogram density)}
  \item{mu }{ the mean of x}
  \item{sd }{ the std dev x}
}
\references{
To add
}
\author{
John Minter <jrminter@gmail.com>
}
\note{
To add
}

%% ~Make other sections like Warning with \section{Warning }{....} ~

\seealso{
%% ~~objects to See Also as \code{\link{help}}, ~~~
}
\examples{
require(analab)
## data
data("diam", package = "analab")
his <- normal.bin(diam[,1])
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{binning}
\keyword{histogram}
\keyword{Gaussian}
\keyword{normal distribution}% __ONLY ONE__ keyword per line
