\name{iLimitsFun}
\alias{iLimitsFun}
\title{ Internal function used to obtain shifted coordinates vector }
\description{
\code{iLimitsFun} receives a numeric vector. Then it returns a vector of length 2*length(x) whose elements are the x values shifted rightward and leftward by 0.5.
}
\usage{
iLimitsFun(i)
}
\arguments{
  \item{i}{ x groups coordinates}
}
\details{
  \code{iLimitsFun} is an internal function, used when plotting spc objects.
}
\value{
	\code{iLimitsFun} returns a vector of length 2*length(x)
}
\references{ Internal function }
\author{ Giorgio Spedicato and Andrea Spano' }
\note{ \code{iLimitsFun} is used by spc object plotting function.
}
\seealso{  \code{\link{plot.spc}}}
\examples{
x=c(2,5,8,4,7)
iLimitsFun(x)
# 1.5 4.5 4.5 7.5 7.5 3.5 3.5 6.5 6.5 7.5
}
\keyword{ internal }
\keyword{ methods }
