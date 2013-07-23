\name{limitsFun}
\alias{limitsFun}
\title{ Internal function to determine y-axis limits }
\description{\code{limitsFun} receives the vector or list of points to be plotted and returns a two elements vector containing the lower and upper limits y-axis limits.}
\usage{limitsFun(list)
}
\arguments{\item{list}{ a vector or list of points. }
}
\details{\code{limitsFun} unlists the input, if it is a list. The limits range given in output is 1.05 times the range between the points given in input.
}
\value{\code{limitsFun} returns a two elements vector containing the lower and the upper limits.
}
\references{ \code{limitsFun} is an internal function }
\author{ Andrea Spano' }
\note{  \code{limitsFun} is used by plot.spc
}
\seealso{ \code{\link{spc}} }
\examples{
##simple example
x=c(2,5,8,4,7)
limits=limitsFun(x)
limits
# 1.7 8.3
}
\keyword{ methods }
\keyword{ internal }
