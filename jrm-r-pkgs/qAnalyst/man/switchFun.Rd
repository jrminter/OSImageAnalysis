\name{switchFun}
\alias{switchFun}
\title{ Internal function to correct evident mispellings }
\description{
  \code{switchFun} returns the correct parse of the command given by the user, according to a specified context.
}
\usage{
switchFun(type, argument)
}

\arguments{
  \item{type}{ The context of user input, either "chart" or "distribution".}
  \item{argument}{ The user input.}
}
\details{

Within argument "chart", following mistakes are identified:
\itemize{
\item "XBAR", "X-BAR", "x-bar" for"xbar"
\item "range" for "r"
\item "sd" for "s"
\item "individuals" and "individual" for "i"
\item "moving range" for "mr"
}

Within argument "distribution", following mistakes are identified:
\itemize{
\item "normal", "normale", "dnorm" for "norm"
\item "dweibull" for "weibull"
\item "log-normal", "dlnorm" and "lognormal" for "lnorm"
}
}
\value{Either a character containing the correct codification or the user input if there is no coded correction.}
\references{ Internal function }
\author{ Giorgio Spedicato }
\note{ This is an internal function.}
\seealso{ \code{\link{spc}}}
\examples{
switchFun(argument="x-bar", type="chart")
}
\keyword{ methods }
\keyword{ internal }
