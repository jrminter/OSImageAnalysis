# v.u.cl.R
#
# this function computes the upper 95% confidence
# limit for a vector

v.u.cl <- function(x){
  # 95% CI from t-distribution
  # from www.cyclismo.org/tutorial/R/confidence.html
  error <- v.std.err(x)*qt(0.975, df=length(x))
  ci.x.ul <- mean(x)+error
  ci.x.ul
}