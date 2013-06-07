\name{lognormal.bin}
\alias{lognormal.bin}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{
A function to bin data and compute parameters for a single mode lognormal distribution
}
\description{
Computes equally-spaced logarithmic bins from a vector and computes the parameters for a single mode lognormal distribution.
}
\usage{
lognormal.bin(x, do.plot = FALSE, n.root.2 = 8)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
A vector of observations
}
  \item{do.plot}{
A Boolean - determines whether the histogram is plotted
}
  \item{n.root.2}{
The bin size - the nth root of 2
}
}
\details{
%%  ~~ If necessary, more details than the description above ~~
}
\value{
A list containing
  \item{data }{a data frame with log.x (log bin midpoint), x (bin midpoint), cts (counts), dens (histogram density)}
  \item{l.mu }{ the mean of log(x). Note: geom mean is exp(l.mu)}
  \item{l.sd }{ the std dev of log(x). Note: geom std dev is exp(l.sd)}
%% ...
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
To add
}
\examples{
require(analab)
## data
data("diam", package = "analab")
l.b <- lognormal.bin(diam[,1])
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{binning}
\keyword{histogram}
\keyword{lognormal distribution}% __ONLY ONE__ keyword per line
