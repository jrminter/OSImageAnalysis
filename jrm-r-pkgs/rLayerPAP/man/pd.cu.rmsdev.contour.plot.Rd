% Generated by roxygen2 (4.1.1): do not edit by hand
% Please edit documentation in R/pd.cu.rmsdev.contour.plot.R
\name{pd.cu.rmsdev.contour.plot}
\alias{pd.cu.rmsdev.contour.plot}
\title{Contour plot for Pd/Cu K-Ratio RMS-deviation}
\usage{
pd.cu.rmsdev.contour.plot(data, lab.cex = 0.9, icp = "", pdf = "")
}
\arguments{
\item{data}{A data frame with tPd, tCu, and RMSdev values \code{data}}

\item{lab.cex}{Optional size for label \code{lab.cex}}

\item{icp}{Optional string with ICP values \code{icp}}

\item{pdf}{Optional string with path for a PDF of the plot\code{pdf}}
}
\value{
A plot
}
\description{
Prepare a contour plot from a data frame containing the RMS deviation
Pd and Cu K-ratios from model values as a function of Pd and Cu thickness.
Optionally save a PDF.
}
\examples{
### Not run
}
\keyword{keywords}

