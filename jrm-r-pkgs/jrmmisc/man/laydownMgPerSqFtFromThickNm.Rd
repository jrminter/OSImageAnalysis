\name{laydownMgPerSqFtFromThickNm }
\alias{
laydownMgPerSqFtFromThickNm 
}
\title{
Compute the laydown of a coated layer from the thickness and density
}
\description{
A helper function to compute the the laydown (mg/ft^2) from the thickness (nm) and density (g/cm^3)
}
\usage{
laydownMgPerSqFtFromThickNm (t.nm, density)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{t.nm}{
The coating thickness nm.
}
  \item{density}{
The density (grams per cubic cm).
}
 
}
\value{
The laydown  (mg/sq.ft.).
}
\author{
J. R Minter
}

\examples{
# For Ni from ICP data
laydown <- laydownMgPerSqFtFromThickNm (112.6, 8.90)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{manip}
