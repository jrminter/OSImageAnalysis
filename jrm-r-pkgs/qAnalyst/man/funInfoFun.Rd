\name{funInfoFun}
\alias{funInfoFun}
\title{ Function to estimate distribution quantities }
\description{
\code{funInfoFun} receives a vector of data and a hyphotized distribution. It estimates hyphotized distribution parameters.
Anderson Darling statistics is provided, if desidered.
}
\usage{
funInfoFun(x, fun, adStats = TRUE)
}
\arguments{
  \item{x}{ a vector of data }
  \item{fun}{ name of function density. This name is processed internally by \code{switchFun}. }
  \item{adStats}{ boolean value to specify if Anderson Darling statistics shall be calculated.}
}
\details{
\code{funInfoFun} uses \code{switchFun} to parse given fun argument into R internal distribution nomenclature. \code{funInfoFun} calls MASS function \code{fitdistr} to estimate parameters (via maximum likelihood). If required \code{andersonDarlingFun} function is called to obtain goodnes of fit statistic and corresponding p-value. 
The returned list contains items that are the corresponding distribution functions to obtain random numbers, quantiles and density.}
\value{
A list containing the following items:
  \item{densfun }{distribution name as specified by user}
  \item{theta }{named vector containing user specification}
  \item{theta }{named vector containing parameter specification}
  \item{qfun }{corresponding internal r function to obtain quantiles}
  \item{dfun }{corresponding internal r function to obtain density}
  \item{rfun }{corresponding internal r function to obtain random values}
  \item{pfun }{corresponding internal r function to obtain CDF}
}
\references{ Venables, W. N. and Ripley, B. D. (2002) Modern Applied Statistics with S. Fourth edition. Springer. }
\author{ Giorgio Spedicato }
\note{ \code{funInfoFun} returns a vector of class "infoFun".
}
\section{Warning}{\code{funInfoFun} estimates parameters by maximum likelihood. Numerical MLE may not always converge. Warning message are thrown in such case. 
Moreover, user shall check that \code{x} vector values lie in the natural support of the distribution specified in \code{fun}}
\seealso{  \code{\link{andersonDarlingFun}}, \code{\link{probplot}} }
\examples{
data(warpTiles)
infoX=funInfoFun(x=warpTiles$warping, fun="weibull")
str(infoX)
}
\keyword{ methods }

