\name{thickNmFromMgPerSqFt}
\alias{
thickNmFromMgPerSqFt
}
\title{
Compute the thickness of a coated layer from the laydown and density
}
\description{
A helper function to compute the thickness of a coated layer from the laydown (mg/ft^2) and density (g/cm^3)
}
\usage{
thickNmFromMgPerSqFt(mg.sq.ft, density)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{mg.sq.ft}{
The coating laydown in mg per sq. ft.
}
  \item{density}{
The density (grams per cubic cm).
}
 
}
\value{
The layer thickness (nm).
}
\author{
J. R Minter
}

\examples{
# For Ni from ICP data
thick <- thickNmFromMgPerSqFt(16.0, 8.90)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{manip}
