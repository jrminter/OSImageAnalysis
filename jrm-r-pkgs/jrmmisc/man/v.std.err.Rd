\name{v.std.err}
\alias{
v.std.err
}
\title{
Compute the standard error for a vector
}
\description{
Computes the standard error of a vector, x.
}
\usage{
v.std.err(x)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
The vector to process.
}
 
}
\value{
Returns the standard error.
}
\author{
J. R Minter
}

\examples{
x <- c(1.1, 1.2, 1.05, 1.07, 0.99, 0.995, 0.98)
ret <- v.std.err(x)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{distribution}
