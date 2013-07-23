\name{statsSpcFun}
\alias{statsSpcFun}

\title{ Internal function to calculate control chart general statistics }
\description{
\code{statsSpcFun} receives data and desidered chart informations. StatsFun returns a list whose elements are general and chart - specific statistics.
}
\usage{
statsSpcFun(x, sg, type = type)
}
\arguments{
  \item{x}{ data vector. }
  \item{sg}{ subgroups id, as specified in \code{\link{spc}} }
  \item{type}{ chart type. }
}
\details{
The type of chart is compulsory.
}
\value{
A list with the following items:
  \item{numTot }{total number of elements in x.}
  \item{numNNmissing }{total number of non - missing elements in x.}
  \item{numMissing }{total number of missing elements in x.}
  \item{nGroupsX }{total number of groups in x.}

  \item{meanX }{mean of x.}
  \item{minX}{min of x.}
  \item{maxX}{max of x.}

  \item{sdTotX }{total standard deviation of x.}
  \item{sdWithinX}{sd within of x.}
  \item{sdBetweenX}{sd between of x.}
  \item{meanRangeX}{mean range of x.}
  
}
\references{ Internal function}
\author{ Giorgio Spedicato}
\note{ Return a list used by spc.}
\seealso{  \code{\link{spc}}, \code{\link{print.spc}} }
\examples{#simple example
set.seed(100)
x=c(rnorm(30,m=10,s=1), rnorm(30,m=12,s=1), rnorm(30,m=10,s=4))
sg=sort(rep(1:30,3))
statsList=statsSpcFun(x=x, sg=sg, type = "xbar")
str(statsList)
}
\keyword{ methods }
\keyword{ internal }
