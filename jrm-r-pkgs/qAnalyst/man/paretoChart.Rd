\name{paretoChart}
\alias{paretoChart}
\title{ function to plot Pareto charts }
\description{
\code{paretoChart} plots Pareto charts for categorical variables. Plot is perfomed by lattice graphics.
}
\usage{
paretoChart(x, mergeThr = 0.9, addLine = TRUE, abbrev = FALSE)
}
\arguments{
  \item{x}{ data vector treated as character variable }
  \item{mergeThr}{ cumulated probability after which categories are merged into generic category "Other".}
  \item{addLine}{ boolean. If true, cumulated frequency line is plot out}
  \item{abbrev}{boolean. If true, abbreviation of categories names written on x axis is done to obtain a better print.}
}
\details{ Different categories are sorted by absolute frequency in decreasing order.
Categories with same absolute frequency are sorted according to their appearing order in the given vector.
 }
\value{
\code{paretoChart} returns no value}
\references{ Montgomery, statistical quality control }
\author{ Giorgio Spedicato }
\note{ A great part of this code comes from pareto.chart function of Luca Scrucca's qcc package.}
\seealso{No see also  }
\examples{
#MASS data set example
require(MASS)
data(Cars93)
paretoData=Cars93$Manufacturer[1:45]
paretoChart(x=paretoData,mergeThr=.8)
}
\keyword{ methods }

