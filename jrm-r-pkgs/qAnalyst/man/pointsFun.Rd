\name{pointsFun}
\alias{pointsFun}
\title{ Internal function to obtain y coordinates of the statistics to be plotted on chosen chart type }
\description{
\code{pointsFun} receives chart specifications and returns the vector of the points to be plotted.
}
\usage{
pointsFun(x, sg, type = "xbar")
}
\arguments{
  \item{x}{ data vector }
  \item{sg}{ Subgroup id variable }
  \item{type}{ type of chart }
}
\details{
\code{pointsFun} calculates the points to be plotted onto the chart according to given chart specification. The vector returned by \code{pointsFun} is therefored saved into the spc object that called \code{pointsFun}.
}
\value{
a vector of values }
\references{ Internal function }
\author{ Andrea Spano' and Giorgio Spedicato }
\note{ This is an internal function
}
\seealso{  \code{\link{spc}}, \code{\link{clFun}} }
\examples{

#brakeCap
data(brakeCap)
x=brakeCap$hardness
sg=brakeCap$subgroup
pointsFun(x=x,sg=sg,type="xbar")

}
\keyword{ methods }
\keyword{ internal }
