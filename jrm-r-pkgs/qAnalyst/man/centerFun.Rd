\name{centerFun}
\alias{centerFun}
\title{ Internal function to calculate center line values }
\description{
\code{centerFun} calculates and returns the center line constant for the given chart type.
}
\usage{
centerFun(x, sg, type = "xbar", mu = NA, sigma = NA)
}

\arguments{
  \item{x}{ data vector. }
  \item{sg}{ subgroups id for variables chart, subgroups dimension for attributes chart, interval dimension for i/mr chart. A detailed description of sg field is in \code{\link{spc}} function help.}
  \item{type}{ chart type. }
  \item{mu}{A scalar containing the process mean. Its use will be different depending from chart type. For more details see \link{spc}.}
  \item{sigma}{A scalar containing the process within samples standard deviation. For more details see \link{spc}.}
}
\details{
\code{centerFun} calculates the center line value. Formulas used are taken from quoted reference book.
}
\value{
  A numeric value for the center line.
}
\references{ Montgomery, Statistical Quality Control }
\author{ Andrea Spano' and Giorgio Spedicato }
\note{ 
\code{centerFun} is called internally by spc.
}
\seealso{ \code{\link{spc}}, \code{\link{clFun}} }
\examples{
#brakeCap dataset
data(brakeCap)
centerFun(x=brakeCap$hardness, sg=brakeCap$subgroup, type="xbar")
}
\keyword{ methods }
\keyword{ internal }
