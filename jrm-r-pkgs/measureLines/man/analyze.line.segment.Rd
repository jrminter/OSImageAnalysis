\name{analyze.line.segment}
\alias{
analyze.line.segment
}
\title{Analyze a data frame from a single line segment
}
\description{
Analyze a data frame from a single line segment and return
a list with summary statistics.
}
\usage{
analyze.line.segment(name, dat, iDigits=4)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{name}{
The identifier for this segment.
}
  \item{dat}{
A data frame containing all 12 edges. 
}
  \item{iDigits}{
Rounding precision
}
}
\value{
A list with line width (mean, se), raggedness (left, right),
sharpness (left mean, left se, right mean, right se)
}
\author{
J. R Minter
}

\examples{
# To do
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{models}
