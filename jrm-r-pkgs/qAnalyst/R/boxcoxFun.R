boxcoxFun = function(x) {
  # Check if all values are positive
  checkPositivity = ifelse(x > 0, TRUE, FALSE)
  if (!all(checkPositivity)) stop("Error! All x must be positive")


  # Creates bc object by powerTransform of car package
  bcObj = powerTransform(x)
  lambda = coef(bcObj)

  y = bcPower(x, lambda = coef(bcObj))
  y = y[!is.na(y)]

  outList = list(type = "boxcox", parameters = lambda, original = x, transformed = as.numeric(y))
  class(outList) = "transformation"
  invisible(outList)
}
