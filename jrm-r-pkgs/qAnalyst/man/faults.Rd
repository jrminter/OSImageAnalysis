\name{faults}
\alias{faults}
\docType{data}
\title{ Variability of faults during week shift}
\description{
Faults dataframe contains measured faults during weekly shifts. There are three shifts per week.
}
\usage{data(faults)}
\format{
  A data frame with 100 observations on the following 2 variables.
  \describe{
    \item{\code{faults}}{fault measures.}
    \item{\code{shift}}{shift id.}
  }
}
\details{
Each shift can be used as subgroups id.
}
\source{
Industrial data.
}
\references{
Faults dataframe can be used to show an application of s-bar chart.
}
\examples{
data(faults)
schart=spc(x=faults$faults, sg=faults$shift, type="s", name="faults")
plot(schart)
}
\keyword{datasets}
