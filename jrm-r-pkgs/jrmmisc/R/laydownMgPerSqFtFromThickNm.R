laydownMgPerSqFtFromThickNm <- function(t.nm, density){
  t.cm <- 1.0e-07 * t.nm
  g.sq.cm <- density * t.cm
  mg.sq.ft <- 9.29e5 * g.sq.cm
  mg.sq.ft
}

# Unit test from ICP 112.6 nm Ni -> 93.1 mg/sq ft
# print(laydownMgPerSqFtFromThickNm(112.6, 8.90))