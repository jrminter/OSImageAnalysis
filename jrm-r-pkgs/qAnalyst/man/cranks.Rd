\name{cranks}
\alias{cranks}
\docType{data}
\title{ Cranks data set}
\description{
Cranks dataframe comes from an engines assembly department, where the deviation from an ideal position of a parts of the crankshaft are measured daily.
}
\usage{data(cranks)}
\format{
  A data frame with 125 observations on the following 2 variables.
  \describe{
    \item{\code{crankshaft}}{Distance in millimeters from the actual point of the crankshaft to the baseline position.}
    \item{\code{workingDay}}{Working day of the relevation. This is the subgroup id.}
  }
}
\details{
Subgroups dimensions are not equal.
}
\source{
Industrial data.
}
\references{Cranks dataset can be used to show subgroups charts capabilities}
\examples{
data(cranks)
xbarchart=spc(x=cranks$crankshaft, sg=cranks$workingDay, type="xbar", name="crankshaft")
rbarchart=spc(x=cranks$crankshaft, sg=cranks$workingDay, type="r", name="crankshaft")
plot(xbarchart)
plot(rbarchart)
}
\keyword{datasets}
