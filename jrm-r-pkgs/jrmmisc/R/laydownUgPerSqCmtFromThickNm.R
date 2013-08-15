laydownUgPerSqCmtFromThickNm <- function(t.nm, density){
  t.cm <- 1.0e-07 * t.nm
  g.sq.cm <- density * t.cm
  ug.sq.cm <- 1.0e6 * g.sq.cm
}

# Unit test from Pouchou 2002a for Zn 36 nm -> 26 ug/sq.cm
# print(laydownUgPerSqCmtFromThickNm(36, 7.14))
