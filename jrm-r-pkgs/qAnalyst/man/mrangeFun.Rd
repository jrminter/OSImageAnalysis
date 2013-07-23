\name{mrangeFun}
\alias{mrangeFun}

\title{ Internal function to calculate moving range vector }
\description{
\code{mrangeFun} returns the moving ranges vector of specified interval from an input vector x.
}
\usage{
mrangeFun(x, sg = 1)
}

\arguments{
  \item{x}{ individual values vector }
  \item{sg}{ interval width, default 1 }
}
\details{
  NA elements are present in the first interval elements of the returned vector as moving range is not defined there.
}
\value{
A numeric vector of moving ranges.
}
\references{ internal function }
\author{ Giorgio Spedicato }
\note{ Internal function
}
\seealso{  \code{\link{clFun}}, \code{\link{centerFun}}}
\examples{
#simple example
a=c(1,3,5,2,6,2,6,8,2)
print(mrangeFun(a,2))
}

\keyword{ methods }
\keyword{ internal }
