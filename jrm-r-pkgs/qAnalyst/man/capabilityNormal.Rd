\name{capabilityNormal}
\alias{capabilityNormal}
\title{Computing Capability Analysis for Normal data}
\description{
 \code{capabilityNormal} is used to compute capability analysis for normal distributed data. This function creates a capability class object for normal data. \code{plot}, \code{print} and \code{summary} methods are avaible for capability class objects.
}
\usage{
capabilityNormal(x, sg=length(x), lsl = NULL, usl = NULL, target = NULL,
    name = deparse(substitute(x)), toler=6, historicalMean=NA, historicalSd=NA)
}

\arguments{
  \item{x}{Numeric data vector }
  \item{sg}{ Subgroup specification. It represents rational sub-group of observations. It can be specified either as a vector, of the same length of \code{x} of ordered subgroup id, or as a constant indicating subgroup size. Default is sg=length(x).}
  \item{lsl}{ Lower specification limit. }
  \item{usl}{ Upper specification limit. }
  \item{target}{ Process target. }
  \item{name}{ Variable label to be used within graphics, default taken by "x" name. }
  \item{toler}{Width of tolerance specification. Default is 6}
  \item{historicalMean}{Mean of the population distribution if a known process parameter is available or an estimate obtained from past data. If mean value is not specified, it is estimated from data } 
  \item{historicalSd}{ Standard Deviation of the population distribution if a known process parameter is available or an estimate obtained from past data. If value of standard deviation is not specified, it is estimated from data   } 
}

\details{
  Either lsl or usl must be specified. 
}
\value{ An object of class capability }
\references{ Bothe (1997), Measuring Process Capability, McGraw Hill }
\author{ Andrea Spano'}
\note{No notes}
\seealso{ \code{\link{plot.capability}}, \code{\link{print.capability}}, \code{\link{summary.capability}} }
\examples{
data(brakeCap)
capObj=capabilityNormal(x=brakeCap$hardness,sg=brakeCap$subgroup, lsl=39,
    usl=41, target=40,  name="HARDNESS")
summary(capObj)
  }
\keyword{ methods }
