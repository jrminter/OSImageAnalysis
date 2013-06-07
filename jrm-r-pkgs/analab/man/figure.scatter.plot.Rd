\name{figure.scatter.plot}
\alias{figure.scatter.plot}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{
Generate a scatter plot for a figure
}
\description{
Generate a scatter plot for a beamer slide or a figure where the title is supplied in the caption or slide title.
}
\usage{
figure.scatter.plot(x, y, lab.x = "x", lab.y = "y", lab.cex = 1.6, ax.cex = 1.6, ax.lw = 3, pts.cex = 1.6, pts.lw = 2, pts.pch = 1, pts.col = "blue", new.mar = c(4.7, 4.7, 1.1, 1.8), fixed.scale = FALSE, x.lim = c(0, 100), y.lim = c(0, 100), ...)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
a vector containing the independent variable
}
  \item{y}{
A vector containing the dependent variable
}
  \item{lab.x}{
A label for the x-axis
}
  \item{lab.y}{
A label for the y-axis
}
  \item{lab.cex}{
scale factor for the labels
}
  \item{ax.cex}{
scale factor for the axis
}
  \item{ax.lw}{
line width for the axis
}
  \item{pts.cex}{
scale factor for the points
}
  \item{pts.lw}{
line width for the point
}
  \item{pts.pch}{
code for point symbol
}
  \item{pts.col}{
color for the points
}
  \item{new.mar}{
a vector with the margin parameters
}
  \item{fixed.scale}{
a boolean. TRUE to use manual axis scaling
}
  \item{x.lim}{
a vector for range of x-axis
}
  \item{y.lim}{
a vector for range of y-axis
}
  \item{\dots}{
other graphics parameters
}
}
\details{
Just a wrapper function in the spirit of DRY
}
\value{
Just the plot to the graphics device.
}
\references{
None
}
\author{
John Minter <jrminter@gmail.com>
}
\note{
Maybe later
}

%% ~Make other sections like Warning with \section{Warning }{....} ~

\seealso{
Perhaps later 
}
\examples{
require(analab)
r <- (1:15)/15
s <- r^2
figure.scatter.plot(r,s)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{scatterplot}
\keyword{figure}% __ONLY ONE__ keyword per line
