\name{brakeCap}
\alias{brakeCap}
\docType{data}
\title{ Brake capability dataset}
\description{
  \code{BrakeCap} dataframes contains shoes brakes physical proprieties: hardness, centering, quencing. 50 batches of 5 elements each have been sampled.
}
\usage{data(brakeCap)}
\format{
  A data frame with 250 observations on the following 4 variables:
  \describe{
    \item{\code{hardness}}{brake hardness}
    \item{\code{centering}}{brake centering}
    \item{\code{quencing}}{brake quencing}
    \item{\code{subgroup}}{brake subgroup}
  }
}
\details{
  This dataset contains both measurement data both subgroups information
}
\source{
 Industrial data
}
\references{
  Industrial data
}
\examples{
data(brakeCap)
#x-bar control chart
hadnessSPCxb=spc(x=brakeCap$hardness, sg=brakeCap$subgroup, type="xbar", name="hardness")
plot(hadnessSPCxb)
summary(hadnessSPCxb)
#r control chart
hadnessSPCr=spc(x=brakeCap$hardness, sg=brakeCap$subgroup, type="r", name="hardness")
plot(hadnessSPCr)
summary(hadnessSPCr)
#process in control
#ok for
#capability analysis
hadnessCap=capabilityNormal(x=brakeCap$hardness, sg=brakeCap$subgroup, lsl=39, usl=41, 
    target=40.5, name="hardness")
summary(hadnessCap)
plot(hadnessCap)
}
\keyword{datasets}
