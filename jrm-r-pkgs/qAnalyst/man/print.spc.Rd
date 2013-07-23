\name{print.spc}
\alias{print.spc}
\title{Print method for spc object }
\description{\code{print.spc} implements generic print function to spc object.
}
\usage{
\method{print}{spc}(x, \dots)
}

\arguments{
\item{x}{an object of class spc}
\item{...}{further arguments to be added}
}
\details{  \code{prints.spc} prints out brief informations on spc object.
}
\value{
This function does not return any value.
}
\references{No references}
\author{ Andrea Spano' }
\note{ Printed informations are general statistics.
}
\seealso{ \code{\link{spc}}, \code{\link{plot.spc}} }
\examples{
#data brakeCap

data(brakeCap)
x=brakeCap$quencing
sg=brakeCap$subgroup

go=spc(x=x,sg=sg,type="xbar", testType=2, k=0,p=0,nSigma=0)
plot.spc(go)
print.spc(go)
rm(go)
}
\keyword{methods}

