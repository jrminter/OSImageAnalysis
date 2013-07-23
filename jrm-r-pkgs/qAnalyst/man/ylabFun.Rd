\name{ylabFun}
\alias{ylabFun}

\title{ Internal function to make labels for y axis }
\description{
\code{ylabFun} makes y-axis labels.
}
\usage{
ylabFun(xName, type = "xbar")
}

\arguments{
  \item{xName}{ is the name of the analyzed variable. }
  \item{type}{ type of chart to be plotted, default "xbar". Specified chart type must have been implemented. }
}
\details{
This is an internal function.
}
\value{
A string that concatenates chartType of xName.
}
\references{ Internal function }
\author{ Giorgio Spedicato }
\note{ Internal function
}
\seealso{  \code{\link{spc}}, \code{\link{plot.spc}} }
\examples{
type="i"
xName="weight"
print(ylabFun(xName,type))
#"Individual values of weight"
}
\keyword{ methods}
\keyword{ internal}
