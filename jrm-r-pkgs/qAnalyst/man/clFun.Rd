\name{clFun}


\alias{clFun}


\title{Internal function to compute upper or lower confidence limits for the specified control chart}


\description{
  \code{clFun} calculates upper and lower confidence limits for control charts. Confidence limits are retuned as a vector.
}


\usage{
  clFun(x, sg, nSigma, cl, type = "xbar", xbarVariability = "auto", mu = NA, sigma = NA)
}


\arguments{
 \item{x}{data vector}

  \item{sg}{
    Subgroup variable. This argument has a different meaning according to chart type.

    \code{xbar}, \code{r} and \code{s} charts: \code{sg} represents rational sub-group of observations. It can be specified either as a vector, of the same length of \code{x} of ordered subgroup id, or as a constant value that will be replicated along x. Subgroup dimension must be greather than one.

    \code{i} and \code{mr} charts: \code{sg} represents the width of the window over which moving range are computed. Must be a scalar. Default value is set to two.

    \code{p}, \code{np} and \code{u} charts: \code{sg} represents sample size of observation. It can be specified either as a vector, of the same length of \code{x} or as a constant value that will be replicated along x.

    \code{c} chart: \code{sg} is not required

  }

  \item{nSigma}{A vector or a scalar of parameters to be used by tests. If \code{nSigma} is not specified, tests are performed with \code{nSigma} default values. If \code{nSigma} is specified, its length must be of the same length as \code{testType}.}
  
  \item{cl}{ "u" or "l" respectively for upper or lower confidence limit}

  \item{type}{Chart type. String identifying chart type. Charts can be of type: "xbar", "r", "s", "i", "mr", "p", "np", "u", "c".}

  \item{xbarVariability}{
    How to compute variability for xbar charts.

    \code{"auto"}: (default) use the ranges if all subgroups have the same numerosity, and it is less than 7; otherwise it use the standard deviations.

    \code{"r"}   : use the ranges for the variaibility of the xbar charts.

    \code{"s"}   : use the standard deviations for the variability of the xbar charts.
  
  }

  \item{mu}{
    A scalar containing the process mean. Its use will be different depending from chart type.

    \code{xbar} and \code{i} charts: mu represents the center line. If \code{mu} is specified also \code{sigma} must be specified. If \code{mu} is not specified, then the process mean is calculated from data.

    \code{p}, \code{np}, \code{c} and \code{u} charts: mu represents the parameter value for the in-control process, and then the center line. If \code{mu} is not specified, then the process mean is calculated from data. 

    \code{s}, \code{r} and \code{mr} charts: \code{mu} is not used.
  }

  \item{sigma}{
    A scalar containing the process within samples standard deviation. Its use will be different depending from chart type.

    \code{xbar} and \code{i} charts: the within samples variability around the center line. If \code{sigma} is specified also \code{mu} must be specified. If \code{sigma} is not specified, then the process within samples standard deviation is calculated from data.

    \code{s} chart: \code{sigma} represents the center line. If \code{sigma} is not specified, then the process standard within samples deviation is calculated from data.

    \code{r} and \code{mr} charts: \code{sigma} is used to calculate the center line. If \code{sigma} is not specified, then the process standard within samples deviation is calculated from data.

    \code{p}, \code{np}, \code{c} and \code{u} charts: \code{sigma} is not used.

  }
 
}


\details{
  clFun allows to handle unequal sample size subgroups that makes confidence limits to vary. A warning is thrown if subgroup dimension is less than 2 when variables chart for groups are calculated.
}


\value{A vector of length equal to the number of points in the chart representing either lower o upper confidence limit.}


\references{Montgomery, Statistical Quality Control}


\author{Andrea Spano' and Giorgio Specicato}


\note{Internal function}


\seealso{\code{\link{spc}}, \code{\link{plot.spc}}}


\examples{
# brakeCap dataset
data(brakeCap)
clFun(x=brakeCap$hardness, sg=brakeCap$subgroup, nSigma=2, cl="u", type="xbar")
}


\keyword{methods}
\keyword{internal}
