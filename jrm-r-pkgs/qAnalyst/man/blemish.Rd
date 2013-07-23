\name{blemish}
\alias{blemish}
\docType{data}
\title{ Blemishes on sampled squares of fabric}
\description{
Blemish dataframe comes from a linen manifacturing. 100 square yards of fabric are sampled and blemishes are counted.
}
\usage{data(blemish)}
\format{
  A data frame with 40 observations on the following 2 variables.
  \describe{
    \item{\code{blemish}}{number of blemishes counted}
    \item{\code{linenSampled}}{sample id}
  }
}
\details{
Data from blemish example are suitable to be projected onto a C control chart.
}
\source{
Industrial data.
}
\references{
This type of data can be used within attribute chart presentations.
}
\examples{
data(blemish)
cchart=spc(x=blemish$blemish,  type="c", name="blemish")
plot(cchart)
}
\keyword{datasets}
