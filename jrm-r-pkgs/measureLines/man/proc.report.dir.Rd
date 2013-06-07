\name{proc.report.dir}
\alias{
proc.report.dir
}
\title{
Process all ``.csv'' files in a directory
}
\description{
Process ann the ``.csv'' files in a directory and return
a data frame with summary statistics.
}
\usage{
proc.report.dir(path, n.term.dig=3L, iDigits=5)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{path}{
path to directory where .csv files with data are store,
Must end with a ``/''.
}
  \item{n.term.dig}{
Number of terminal digits ``-ddd.csv'' on the individual
``.csv'' files.  Note: specify like ``3L''.
}
  \item{iDigits}{
Precision for rounding.
}
 
}
\value{
Returns a data frame with summary statistics.
}
\author{
J. R Minter
}

\examples{
# To do...
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{models}
