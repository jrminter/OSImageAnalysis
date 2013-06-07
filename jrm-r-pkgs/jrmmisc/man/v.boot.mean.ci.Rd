\name{v.boot.mean.ci}
\alias{
v.boot.mean.ci
}
\title{
Bootstrap the mean and 95\% confidence interval for a vector
}
\description{
Use the bootstrap to estimate the mean 95\% confidence inteval
for a vector, x, using nSamples. Returns a vector of estimate
(mean, normal lcl, normal ucl, percent lcl, percent ucl).
}
\usage{
v.boot.mean.ci(x, nSamples=999)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{x}{
The vector to process.
}
  \item{nSamples}{
The number of samples (with replacement.)
}
 
}
\value{
Returns a vector of estimates: 
(mean, normal lcl, normal ucl, percent lcl, percent ucl).
}
\author{
J. R Minter
}

\examples{
require(boot)
require(jrmmisc)
z <- rnorm(250)
a <- v.boot.mean.ci(z)
print(a)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{distribution}
