\name{papEta}
\alias{papEta}
\title{Compute the backscattered electron yield for an element}
\usage{
papEta(z)
}
\arguments{
  \item{z}{The atomic number of the element}
}
\value{
the backscattered electron yield
}
\description{
Use the method of Pouchou and Pichoir 1991 to compute the
backscattered electron yield for a given element
}
\examples{
# Compute for Cu
eta <- papEta(29)
}
\keyword{keywords}

