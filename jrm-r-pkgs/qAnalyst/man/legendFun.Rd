\name{legendFun}
\alias{legendFun}
\title{ Internal funtion to calculate trellis legend parameters }
\description{
\code{legendFun} returns a list containing \code{text}, \code{color}, \code{lty} and number of \code{columns} parameters used within trellis plot of a given capabilityObj.
}
\usage{
legendFun(capabilityObj)
}
\arguments{
  \item{capabilityObj}{ A capability obj.}
}
\details{
  Internal function.
}
\value{
A list containing the following items:
  \item{textKey }{text legend items.}
  \item{linesColorKey }{color lines.}
  \item{linesLtyKey }{lines layout.}
  \item{numColumns }{number of columns.}
}
\references{ Internal function. }
\author{ Giorgio Spedicato }
\note{Items in list are used in trellis graphic}
\seealso{  \code{\link{plot.capability}}}
\examples{
#brakeCap data
data(brakeCap)
capObj=capabilityNormal(x=brakeCap$hardness, sg=brakeCap$subgroup, usl=41.5)
legenda=legendFun(capObj)
str(legenda)
}
\keyword{ internal }
\keyword{ methods }
