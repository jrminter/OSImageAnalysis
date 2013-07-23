\name{toys}
\alias{toys}
\docType{data}
\title{ Toys manufacturing data}
\description{
toys dataframe reports control quality results from a toys factory.
}
\usage{data(toys)}
\format{
  A data frame with 80 observations on the following 7 variables.
  \describe{
    \item{\code{day}}{day of ispection}
    \item{\code{weight}}{weight of the sampled toy}
    \item{\code{length}}{length of the sampled toy}
    \item{\code{defects}}{defects on sampled toys}
    \item{\code{sample}}{sampled toys}
    \item{\code{rejects}}{number of toys rejected in ispected toys}
    \item{\code{inspected}}{dimension of inspection sample}
  }
}
\details{
Fields have different lengths, due coming from different ispection processes.
}
\source{
Industrial data.
}
\references{
This dataset can be use to plot different types of control charts. Fields "rejects" and "inspected" may be used to plot np control charts.
}
\examples{
data(toys)
npchart=spc(x=na.omit(toys$rejects), sg=na.omit(toys$inspected), type="np",
    name="Toys rejected")
plot(npchart)
}
\keyword{datasets}
