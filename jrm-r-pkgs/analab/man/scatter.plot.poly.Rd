\name{scatter.plot.poly}
\alias{scatter.plot.poly}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{
scatter.plot.poly
Scatter plots with optional polynomial regression 
}
\description{
A wrapper for level graphics functions to do a scatter plot and perform an optional poynomial regression.
}
\usage{
scatter.plot.poly(x, y, delta=NULL, bErrorBars=FALSE, bReg=FALSE, iReg=2,
                  str.x = "X", str.y="Y", str.title="Plot",
                  v.cex=1.2, a.cex=1.2, t.cex=1.2,
                  lw.fit = 2, lw.pts =2, lw.bars =2, lw.ax = 3,
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
  \item{bReg}{
a boolean to turn off/on polynomial regression
}
  \item{iReg}{
The order of the polynomial ( iReg >= 2)
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
  \item{lw.fit}{
line width of fit
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
There is no point in using iReg < 2. One might want to adjust text sizes and line widths for PDF output.
}
\value{
\item{fit}{The results of the fit}
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

\examples{
library(analab)
# set up simple vectors
ax <- c(1.00, 2.00, 3.00,  4.00,  5.00)
ay <- c(1.05, 4.05, 8.95, 16.05, 24.95)
ad <- c(0.05, 0.03, 0.04, 0.06, 0.05)
# do a plot and polynomial regression with error bars
the.fit <- scatter.plot.poly(ax, ay, ad, bErrorBars=TRUE, bReg=TRUE, iReg = 2)

}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{scatterplot}
\keyword{graphics}% __ONLY ONE__ keyword per line
