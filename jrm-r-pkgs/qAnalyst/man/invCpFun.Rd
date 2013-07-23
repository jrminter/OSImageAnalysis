\name{invCpFun}
\alias{invCpFun}
\title{ Function to get inverse capability tolerance limits }
\description{
\code{invCpFun} returns tolerance limits for a given data vector, provided a desidered cp. 
}
\usage{
invCpFun(x, cp = 1, fun = "normal")
}
\arguments{
  \item{x}{ a vector of data }
  \item{cp}{ desidered cp }
  \item{fun}{ specified distribution, default normal }
}
\details{
Cp is supposed to be equal to cp, that is cp=cpk.
}
\value{
A vector containing lsl and usl for given data.}
\references{ Bothe (1997), Measuring Process Capability, McGraw Hill }
\author{ Giorgio Spedicato and Andrea Spano' }
\note{No notes}
\seealso{ \code{\link{capability}}, \code{\link{funInfoFun}} }
\examples{
#brakeCap example
data(brakeCap)
invCpFun(x=brakeCap$hardness, cp=1, fun="normal")
}
\keyword{ methods }
