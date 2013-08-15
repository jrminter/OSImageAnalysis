\name{laydownUgPerSqCmtFromThickNm}
\alias{
laydownUgPerSqCmtFromThickNm
}
\title{
Compute the laydown of a coated layer from the thickness and density
}
\description{
A helper function to compute the laydown (mg/ft^2) of a coated layer from the thickness (nm) and density (g/cm^3)
}
\usage{
laydownUgPerSqCmtFromThickNm(t.nm, density)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{t.nm}{
The coating thickness in nm.
}
  \item{density}{
The density (grams per cubic cm).
}
 
}
\value{
The laydown (ug/sq.cm).
}
\author{
J. R Minter
}

\examples{
# For Zn from Pouchou 2002a for Zn 36 nm -> 26 ug/sq.cm
laydown <- laydownUgPerSqCmtFromThickNm(36, 7.14)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{manip}
