\name{iFun}
\alias{iFun}

\title{ Internal function to create sequences }
\description{
  \code{iFun} is an internal function to create a sequence from 1 to n, where n=length(x).
}
\usage{
iFun(x)
}
\arguments{
  \item{x}{ a numeric vector }
}
\details{
 iFun is a simple internal function, used by plot method.
}
\value{
a sequence vector.
}
\references{ Internal function }
\author{ Giorgio Spedicato and Andrea Spano' }
\note{ Internal function}
\seealso{ \code{\link{spc}}, \code{\link{plot.spc}} }
\examples{
#very simple example
x=c(4,5,8,2,3)
output=iFun(x)
output
# 1 2 3 4 5
}
\keyword{ methods }
\keyword{ internal }
