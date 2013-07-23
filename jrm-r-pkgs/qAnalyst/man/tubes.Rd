\name{tubes}
\alias{tubes}
\docType{data}
\title{ Tubes for television}
\description{
Tubes dataframe contains data from control quality ispections of tubes for television.
}
\usage{data(tubes)}
\format{
  A data frame with 20 observations on the following 2 variables.
  \describe{
    \item{\code{rejects}}{number of rejected devices during quality ispection.}
    \item{\code{sampled}}{sampled devices during quality inspection.}
  }
}
\details{
Results of twenty quality ispections are reported.
}
\source{
Industrial data.
}
\references{
Content of this dataset can be shown by p-chart.
}
\examples{
data(tubes)
pchart=spc(x=tubes$rejects, sg=tubes$sampled, type="p",
    name="proportion of defective tv tubes")
plot(tubes)
}
\keyword{datasets}
