\name{v.u.cl}
\alias{
v.u.cl
}
\title{
Compute the upper 95\% confidence limit for a vector
}
\description{
Computes the upper 95\% confidence limit for a vector, x.
}
\usage{
v.u.cl(x)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
The vector to process.
}
 
}
\value{
Returns the upper 95\% confidence.
}
\author{
J. R Minter
}

\examples{
x <- c(1.1, 1.2, 1.05, 1.07, 0.99, 0.995, 0.98)
ret <- v.u.cl(x)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{distribution}
