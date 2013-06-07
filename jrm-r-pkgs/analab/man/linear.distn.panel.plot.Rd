\name{linear.distn.panel.plot}
\alias{linear.distn.panel.plot}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{
A three panel plot with linear binning
}
\description{
computes a histogram with linear binning, plotting the mean and kernel density as well. Does a boxplot and a qqplot, all in a single panel.
}
\usage{
linear.distn.panel.plot(v.dat, n.brks = 50, distn.lab = NULL, hist.legend = TRUE, legend.loc = "topright", kern.bw = "nrd0", plt.median = TRUE, scale.mult = 1.2, ...)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{v.dat}{
A data vector
}
  \item{n.brks}{
Number of breaks for the histogram 
}
  \item{distn.lab}{
The label for the data
}
  \item{hist.legend}{
plot a histogram legent
}
  \item{legend.loc}{
location for the histogram legend
}
  \item{kern.bw}{
the kernel for the density smoothing
}
  \item{plt.median}{
A boolean to plot the median value on the histogram
}
  \item{scale.mult}{
A scale multiplier - get the legend above the data
}
  \item{\dots}{
Other graphical parameters...
}
}
\details{
%%  ~~ If necessary, more details than the description above ~~
}
\value{
Returns a plot to the current graphics device
}
\references{
To do\ldots
}
\author{
J. R. Minter <jrminter@gmail.com>
}
\note{
%%  ~~further notes~~
}

%% ~Make other sections like Warning with \section{Warning }{....} ~

\seealso{
To do
}
\examples{
require(analab)
set.seed(42)
x <- rnorm(1500, mean=25, sd=2.0)
linear.distn.panel.plot(x, n.brks=15, kern.bw="nrd0",
                        distn.lab='diameter [nm]')
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{panel plot}
\keyword{binning}% __ONLY ONE__ keyword per line
