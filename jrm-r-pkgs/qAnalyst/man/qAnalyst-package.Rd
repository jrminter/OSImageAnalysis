\name{qAnalyst-package}

\alias{qAnalyst-package}

\alias{qAnalyst}

\docType{package}

\title{Package to create and analyze control charts and to perform capability analysis}

\description{Creates xbar, s, r, i, mr, p, np, c, u chart. Perform capability analysis for both normal and non normal data.}

\details{

  \tabular{ll}{
    Package: \tab qAnalyst\cr
    Type: \tab Package\cr
    Version: \tab 0.6.5\cr
    Date: \tab 2013-07-23\cr
    License: \tab GPL -2
  }

  Function \code{spc} and \code{capability} create objects of class \code{spc} and \code{capability} respectively. \cr
  Charts of type xbar, r, s, i, mr, p, np, c and may be handled by \code{spc} objects. \cr 
  Generic methods plot, print and summary exist for \code{spc} and \code{capability} objects. \cr

}

\author{
Andrea Spano'
Patched by John Minter \email{jrminter@gmail.com}

Maintainer: Andrea Spano' \email{andrea.spano@quantide.com}
}

\references{
Montgomery, Statistical Quality Control
}

\keyword{package}

\examples{
# A simple x bar chart
# Data: cranks

data(cranks)
x = cranks$crankshaft
sg = cranks$workingDay

go = spc(x = x, sg = sg, type = "xbar")
plot(go)
print(go)
summary(go)
rm(go)


# Capability example
# Data: cranks
data(cranks)
x = cranks$crankshaft
sg = cranks$workingDay

go = capabilityNormal(x = x, sg = sg, lsl = -10, usl = 10, target = 0)
plot(go)
print(go)
summary(go)
rm(go)
}
