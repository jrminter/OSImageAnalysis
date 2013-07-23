\name{spc}


\alias{spc}


\title{Function to create spc object}


\description{
  \code{spc} function creates spc class objects from data. Generic methods \code{plot}, \code{print}, \code{summary} are avaiable for SPC class objects.
}


\usage{
  spc(x, sg = NULL, type = "xbar", xbarVariability = "auto", name = deparse(substitute(x)), testType = 1, 
      k = NA, p = NA, nSigma = 3, mu = NA, sigma = NA)
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

  \item{type}{Chart type. String identifying chart type. Charts can be of type: "xbar", "r", "s", "i", "mr", "p", "np", "u", "c".}

  \item{xbarVariability}{
    How to compute variability for xbar charts.

    \code{"auto"}: (default) use the ranges if all subgroups have the same numerosity, and it is less than 7; otherwise it use the standard deviations.

    \code{"r"}   : use the ranges for the variaibility of the xbar charts.

    \code{"s"}   : use the standard deviations for the variability of the xbar charts.
  
  }

  \item{name}{Name of x variable as it appears in the charts. By default the name of the given x variable.}

  \item{testType}{
    A vector or a scalar of test codes to be performed. Eight tests are implemented corrensponding to codes 1-8. Default performed test is 1.

    test 1: At least \code{k} out of \code{p} points in a row beyond Zone A (outside the control limits). Default values: \code{k = p = 1, nSigma = 3}.

    test 2: At least \code{k} out of \code{p} points in a row on one side of central line. Default values: \code{k = p = 9}.

    test 3: At least \code{k} out of \code{p} points in a row all increasing or all decreasing. Default values: \code{k = p = 6}.

    test 4: At least \code{k} out of \code{p} points in a row all up and down. Default values: \code{k = p = 14}.

    test 5: At least \code{k} out of \code{p} points in a row in Zone A or beyond (> (2/3)*nSigma*sigma from central line; same side of central line). Default values: \code{k = 2, p = 3, nSigma = 3}.

    test 6: At least \code{k} out of \code{p} points in a row in Zone B or beyond (> (1/3)*nSigma*sigma from central line; same side of central line). Default values: \code{k = 4, p = 5, nSigma = 3}.

    test 7: At least \code{k} out of \code{p} points in a row in Zone C (both sides of central line). Default values: \code{k = p = 15, nSigma = 3}

    test 8: At least \code{k} out of \code{p} points in a row with no one in Zone C. Default values: \code{k = p = 8,  nSigma = 3}

  }

  \item{k}{A vector or a scalar of parameters to be used by tests. If \code{k} is not specified, tests are performed with \code{k} default values. If \code{k} is specified, its length must be of the same length as \code{testType}.}

  \item{p}{A vector or a scalar of parameters to be used by tests. If \code{p} is not specified, tests are performed with \code{p} default values. If \code{p} is specified, its length must be of the same length as \code{testType}.}

  \item{nSigma}{A vector or a scalar of parameters to be used by tests. If \code{nSigma} is not specified, tests are performed with \code{nSigma} default values. If \code{nSigma} is specified, its length must be of the same length as \code{testType}.}

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
  \code{spc} function performs coherence tests on subgroups dimension and chart name. Then it calculates graphical parameters, statistics values and test results and stores this values in lists.
}


\value{An object of class spc}


\references{Montgomery, Statistical Quality Control}


\author{Andrea Spano'}


\note{No notes}


\seealso{\code{\link{plot.spc}}, \code{\link{print.spc}}}


\examples{
# xbar and s chart with standard given
data(brakeCap)
xbarchart = spc(x=brakeCap$hardness, sg=brakeCap$subgroup, type="xbar", mu=40, sigma=1)
plot(xbarchart)
summary(xbarchart)
schart = spc(x=brakeCap$hardness, sg=brakeCap$subgroup, type="s", mu=1)
plot(schart)
summary(schart)

# i-chart, moving range to estimate standard deviaiton is equal to 2 points
  # with testType=1 
data(rawWeight)
ichart = spc(x=rawWeight$rawWeight, sg=2, type="i", name="weight", testType=1)
plot(ichart)
summary(ichart)

# u chart with standard given
data(toyCarsDefects)
uchart = spc(x=toyCarsDefects$defects, sg=toyCarsDefects$sampled, type="u",
    name="defects", mu=0.05)
plot(uchart)
summary(uchart)
}


\keyword{methods}

