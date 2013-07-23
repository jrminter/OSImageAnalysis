\name{getParameterFun}
\alias{getParameterFun}

\title{ Internal function to get control chart coefficients }
\description{
\code{getParameterFun} returns the value of a parameter given subgroup size and parameter name.
}
\usage{
getParameterFun(n, parameter)
}

\arguments{
  \item{n}{ subgroups length }
  \item{parameter}{ string containing the name of parameters from A6 table, that is: "A", "A2", "A3", "c4", "c4rec", "B3", "B4", "B5", "B6", "d2", "d2rec", "D3", "D4", "D5", "D6". }
}
\details{
Tabulated values are used if subgroup size is less than 25. Otherwise, Montogmery SQC book's formulas are used.
}
\section{warning}{Montgomery original table does not report values for n=1. Constants "d2" and "d4" for n=1 have been integrated from Wheeler and Chambers (1992).}
\value{
Value of the requested parameter given sample size.
}
\references{ Montgomery, Statistical Quality Control; Wheeler and Chambers (1992). Undenstanding Statistical Process control}
\author{ Andrea Spano'}
\note{No notes}
\seealso{ \code{\link{getCoeffFun}} }
\examples{
#a simple example
getParameterFun(5,"d2")
}
\keyword{ methods }
\keyword{ internal }
