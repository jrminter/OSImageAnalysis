# v.std.err.R
#
# compute the std error of a vector.

v.std.err <- function(x){
  ret <- sd(x)/sqrt(length(x))
  ret
}
