thickNmFromUgPerSqCm <- function(ug.sq.cm, density){
  # compute thickness in nm from laydown in ug/sq cm and
  # density in g/cm3
  g.sq.cm <- ug.sq.cm / 1.0e6
  t.cm <- g.sq.cm/density
  t.nm <- 1.0e7*t.cm
  t.nm
}
