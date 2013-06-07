\name{analab-package}
\alias{analab-package}
\alias{analab}
\docType{package}
\title{
Encapsulates functions for data analysis by analytical scientists.
}
\description{
This package provides functions for data analysis by analytical scientists.
It provides wrapper functions to produce publication quality scientific
scatter plots that encapsulates low-level R graphics.
}
\details{
\tabular{ll}{
Package: \tab analab\cr
Type: \tab Package\cr
Version: \tab 1.4.3\cr
Date: \tab 2013-04-03\cr
License: \tab GPL\cr
LazyLoad: \tab yes\cr
}
Currently the package exports the following functions:

figure.scatter.plot -- A tuneable scatter plot for a figure/slide where the title is in the caption or slide title.

normal.bin -- bin data for a normal distribution.

lognormal.bin -- bin data for a lognormal distribution.

linear.distn.panel.plot -- make a panel plot with a histogram/kernel density plot, a boxplot, and a qqplot.

scatter.plot.line - Does a basic linear regression and optionally plots error bars.

scatter.plot.stats - Plots points, mean, confidence interval, and optionally plots error bars.

scatter.plot.poly - Does a basic linear polynomial regression and optionally plots error bars.

}
\author{
John R.Minter <jrminter@gmail.com>
}
\references{

To be added
}
\keyword{ plot }
\keyword{ graphics }
\seealso{
To be added later
}
\examples{
require(analab)

# set up simple vectors
ax <- c(1.00, 2.00, 3.00, 4.00, 5.00)
ay <- c(1.05, 2.05, 2.95, 4.05, 4.95)
ad <- c(0.05, 0.03, 0.04, 0.06, 0.05)

# a tuneable plot for a figure
figure.scatter.plot(ax,ay)

# a panel plot
set.seed(42)
x <- rnorm(1500, mean=25, sd=2.0)
linear.distn.panel.plot(x, n.brks=15, kern.bw="nrd0",
                        distn.lab='diameter [nm]')

# do a plot and linear regression with error bars
the.fit <- scatter.plot.line(ax, ay, ad, bErrorBars=TRUE, bReg=TRUE)

# set up simple vectors
ax <- c(1.00, 2.00, 3.00, 4.00, 5.00)
ay <- c(1.05, 2.05, 2.95, 4.05, 4.95)
ad <- c(0.05, 0.03, 0.04, 0.06, 0.05)
# do a plot and linear regression with error bars
the.stats <- scatter.plot.stats(ax, ay, ad, bErrorBars=TRUE)

# set up simple vectors
ax <- c(1.00, 2.00, 3.00,  4.00,  5.00)
ay <- c(1.05, 4.05, 8.95, 16.05, 24.95)
ad <- c(0.05, 0.03, 0.04, 0.06, 0.05)
# do a plot and polynomial regression with error bars
the.fit <- scatter.plot.poly(ax, ay, ad, bErrorBars=TRUE, bReg=TRUE, iReg = 2)

}
