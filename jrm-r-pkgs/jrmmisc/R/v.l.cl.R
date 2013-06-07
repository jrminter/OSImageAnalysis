# v.l.cl.R
#
# this function computes the lower 95% confidence
# limit for a vector

v.l.cl <- function(x){
  # 95% CI from t-distribution
  # from www.cyclismo.org/tutorial/R/confidence.html
  error <- v.std.err(x)*qt(0.975, df=length(x))
  ci.x.ll <- mean(x)-error
  ci.x.ll  
}