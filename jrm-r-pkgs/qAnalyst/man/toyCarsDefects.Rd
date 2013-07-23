\name{toyCarsDefects}
\alias{toyCarsDefects}
\docType{data}
\title{ Toys car defects}
\description{
toyCarsDefects dataframe reports sample size and the total number of defectives on sampled toy cars in a toy manifacture.
}
\usage{data(toyCarsDefects)}
\format{
  A data frame with 20 observations on the following 2 variables.
  \describe{
    \item{\code{defects}}{number of defects found.}
    \item{\code{sampled}}{sample size.}
  }
}
\details{Data contained in toyCarsDefects dataframe can be used to show attribute charts proprieties.}
\source{
Industrial data.
}
\references{
This dataset can be shown by a u - chart
}
\examples{
data(toyCarsDefects)
head(toyCarsDefects)
chart=spc(x=toyCarsDefects$defects, sg=toyCarsDefects$sampled, name="defects", type="u")
plot(chart)
}
\keyword{datasets}
