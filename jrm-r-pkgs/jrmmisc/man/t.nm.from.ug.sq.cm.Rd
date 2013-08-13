\name{t.nm.from.ug.sq.cm}
\alias{
t.nm.from.ug.sq.cm
}
\title{
Compute the thickness of a coated layer from the laydown and density
}
\description{
A helper function to compute the thickness of a coated layer from the laydown (ug/cm^2) and density (g/cm^3)
}
\usage{
t.nm.from.ug.sq.cm(ug.sq.cm, density)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{ug.sq.cm}{
The coating laydown in ug/cm^2.
}
  \item{density}{
The density (g/cm^3).
}
 
}
\value{
The layer thickness (nm).
}
\author{
J. R Minter
}

\examples{
# For Zn from Pouchou, Mickrochim Acta, 138, 2002 p. 135. Note the table has 2 typos
thick <- t.nm.from.ug.sq.cm(25.0, 7.14)
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{manip}
