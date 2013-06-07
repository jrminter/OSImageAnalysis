\name{scatter.plot.stats}
\alias{scatter.plot.stats}
\title{
scatter.plot.stats
Scatter plots with optional linear regression 
}
\description{
A wrapper for level graphics functions to do a scatter plot and plot the mean and confidence interval.
}
\usage{
scatter.plot.stats(x, y, delta=NULL, bErrorBars=FALSE, dAlpha=0.95,
                  str.x = "X", str.y="Y", str.title="Plot",
                  v.cex=1.2, a.cex=1.2, t.cex=1.2,
                  lw.stats = 2, lw.pts =2, lw.bars =2, lw.ax = 3,
                  len.bars =0.075)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
A vector of 'X' values
}
  \item{y}{
A vector of 'Y' values
}
  \item{delta}{
A vector of standard deviations
}
  \item{bErrorBars}{
a boolean to turn off/on error bars
}
  \item{dAlpha}{
Confidence interval (i.e. 0.95)
}
  \item{str.x}{
X-Axis title
}
  \item{str.y}{
Y-Axis title
}
  \item{str.title}{
Plot title
}
  \item{v.cex}{
size of axis labels
}
  \item{a.cex}{
size of axis
}
  \item{t.cex}{
size of title
}
  \item{lw.stats}{
line width for mean and confidence limit lines
}
 \item{lw.pts}{
line width of points
}
  \item{lw.bars}{
line width of error bars
}
  \item{lw.ax}{
line width of axis
}
  \item{len.bars}{
length of error bar tops
}
}
\details{
One might want to adjust text sizes and line widths for PDF output.
One can use mtext to format and add results to individual plots...
}
\value{
\item{v.stats}{A vector with the mean and standard deviation, p, lci, uci }
}
\references{
To do...
}
\author{
John Minter
}
\note{
To do...
}

%% ~Make other sections like Warning with \section{Warning }{....} ~

\examples{
library(analab)
# set up simple vectors
ax <- c(1.00, 2.00, 3.00, 4.00, 5.00)
ay <- c(1.05, 2.05, 2.95, 4.05, 4.95)
ad <- c(0.05, 0.03, 0.04, 0.06, 0.05)
# do a plot and regression with error bars
the.stats <- scatter.plot.stats(ax, ay, ad, bErrorBars=TRUE)

}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{graphics}
\keyword{polynomial}% __ONLY ONE__ keyword per line
