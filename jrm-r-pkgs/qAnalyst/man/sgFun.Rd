\name{sgFun}
\alias{sgFun}
\title{ Internal function to create subgroups for spc control charts}
\description{
\code{sgFun} creates suitable subgroups according to chart type. }
\usage{
sgFun(x, sg, type)
}
\arguments{
  \item{x}{ data vector.}
  \item{sg}{ subgroups specification depending by chart type, as passed by \code{spc} and \code{capability}.}
  \item{type}{ chart type.}
}
\details{\code{sgFun} is an internal function called by \code{spc} and \code{capability}. For \code{sg} specification details see \code{\link{spc}} and \code{\link{capability}}. }
\value{
A vector of subgroup id.
}
\references{ Internal function }
\author{ Giorgio Spedicato and Andrea Spano'}
\note{ Internal function
}
\seealso{  \code{\link{spc}}, \code{\link{capability}}}
\examples{
x=c(4,5,6,7,8,3)
sgFun(x=x,sg=2,type="xbar")
}

\keyword{ methods }
\keyword{ internal }
