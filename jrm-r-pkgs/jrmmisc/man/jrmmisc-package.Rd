\name{jrmmisc-package}
\alias{jrmmisc-package}
\alias{jrmmisc}
\docType{package}
\title{
jrmmisc
}
\description{
Miscellaneous functions in the spirit of DRY...
}
\details{
\tabular{ll}{
Package: \tab jrmmisc\cr
Type: \tab Package\cr
Version: \tab 1.0.4\cr
Date: \tab 2013-08-15\cr
License: \tab GPL (>=2) | BSD\cr
}
To do \ldots
}
\author{
John Minter

Maintainer: John Minter <jrminter@gmail.com>
}
\references{
TO DO
}
\keyword{ package }
\examples{
x <- c(1.1, 1.2, 1.05, 1.07, 0.99, 0.995, 0.98)
v.se <- v.std.err(x)
v.ucl <- v.u.cl(x)
v.lcl <- v.l.cl(x)

# For Zn from Pouchou, Mickrochim Acta, 138, 2002 p. 135. Note the table has 2 typos
thick1 <- thickNmFromUgPerSqCm(25.0, 7.14)

# For Ni from ICP data
thick2 <- thickNmFromMgPerSqFt(16.0, 8.90)

# For Zn from Pouchou 2002a for Zn 36 nm -> 26 ug/sq.cm
laydown <- laydownUgPerSqCmtFromThickNm(36, 7.14)

# For Ni from ICP data
laydown <- laydownMgPerSqFtFromThickNm (112.6, 8.90)

}
