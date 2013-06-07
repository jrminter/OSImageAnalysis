\name{linewidthplot}
\alias{
linewidthplot
}
\title{
Plot a given line segment from a data file
}
\description{
Do a plot.
}
\usage{
linewidthplot(dat, thr=2, title="foo", units="microns", iDigits=3)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{dat}{
a data frame with line edges produced by ImageJ or analySIS.
}
  \item{thr}{
Threshold value to use: 1 = ``lo'', 2 = ``med'', and 3 = ``high''.
The fraction of the difference in mean gray background and line
is specified in the image analysis step. 
}
  \item{title}{
A label for the segment
}
  \item{units}{
Scale units. Typically microns or nm.
}
  \item{iDigits}{
Precison for the results. 
}

}
\value{
Returns a plot
}
\author{
J. R Minter
}

\examples{
# To do...
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{hplot}
