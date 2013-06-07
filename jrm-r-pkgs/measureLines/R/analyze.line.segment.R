# analyze.line.segment.R
#
# this function takes a data frame containing the
# left and right edges of line segments produced
# from low, med, or high delta gray thresholds
# and analyzes the line width, raggedness, and sharpness
# outputs a list.
analyze.line.segment <- function(name, dat, iDigits=4){
  df.med.left <- dat[,5:6]
  df.med.left <- df.med.left[complete.cases(df.med.left),]
  df.med.left <- data.frame(l=df.med.left[,2], t=df.med.left[,1])
  
  df.med.right <- dat[,7:8]
  df.med.right <- df.med.right[complete.cases(df.med.right),]
  df.med.right <- data.frame(l=df.med.right[,2], t=df.med.right[,1])
  
  df.lo.left <- dat[,1:2]
  df.lo.left <- df.lo.left[complete.cases(df.lo.left),]
  df.lo.left <- data.frame(l=df.lo.left[,2], t=df.lo.left[,1])
  
  df.lo.right <- dat[,3:4]
  df.lo.right <- df.lo.right[complete.cases(df.lo.right),]
  df.lo.right <- data.frame(l=df.lo.right[,2], t=df.lo.right[,1])
  
  df.hi.left <- dat[,9:10]
  df.hi.left <- df.hi.left[complete.cases(df.hi.left),]
  df.hi.left <- data.frame(l=df.hi.left[,2], t=df.hi.left[,1])
  
  df.hi.right <- dat[,11:12]
  df.hi.right <- df.hi.right[complete.cases(df.hi.right),]
  df.hi.right <- data.frame(l=df.hi.right[,2], t=df.hi.right[,1])
  
  
  df.med.left  <- df.med.left[with(df.med.left, order(l)), ]
  df.med.right <- df.med.right[with(df.med.right, order(l)), ]
  
  df.lo.left  <- df.lo.left[with(df.lo.left, order(l)), ]
  df.lo.right <- df.lo.right[with(df.lo.right, order(l)), ]
  
  df.hi.left  <- df.hi.left[with(df.hi.left, order(l)), ]
  df.hi.right <- df.hi.right[with(df.hi.right, order(l)), ]
  
  left.lm.fit <- lm(df.med.left$t ~ df.med.left$l)
  sum.left.fit <- summary(left.lm.fit)
  left.fit.mean.sq.resid <- mean(sqrt(left.lm.fit$residuals^2))
  
  right.lm.fit <- lm(df.med.right$t ~ df.med.right$l)
  sum.right.fit <- summary(right.lm.fit)
  right.fit.mean.sq.resid <- mean(sqrt(right.lm.fit$residuals^2))
  
  int.right.fit.mu <- sum.right.fit$coef[1]
  int.right.fit.se <- sum.right.fit$coef[3]
  
  int.left.fit.mu <- sum.left.fit$coef[1]
  int.left.fit.se <- sum.left.fit$coef[3]
  
  line.width.mu <- abs(int.left.fit.mu - int.right.fit.mu)
  line.width.se <- line.width.mu * sqrt(
    (int.left.fit.se/int.left.fit.mu)^2 +
      (int.right.fit.se/int.right.fit.mu)^2)
  
  # now compute sharpness
  left.lo.fit   <- lm(df.lo.left$t ~ df.lo.left$l)
  left.hi.fit   <- lm(df.hi.left$t ~ df.hi.left$l)
  right.lo.fit  <- lm(df.lo.right$t ~ df.lo.right$l)
  right.hi.fit  <- lm(df.hi.right$t ~ df.hi.right$l)
  sum.left.lo   <- summary(left.lo.fit)
  sum.left.hi   <- summary(left.hi.fit)
  sum.right.lo  <- summary(right.lo.fit)
  sum.right.hi  <- summary(right.hi.fit)
  
  
  int.left.lo.mu <- sum.left.lo$coef[1]
  int.left.lo.se <- sum.left.lo$coef[3]
  int.left.hi.mu <- sum.left.hi$coef[1]
  int.left.hi.se <- sum.left.hi$coef[3]
  
  int.right.lo.mu <- sum.right.lo$coef[1]
  int.right.lo.se <- sum.right.lo$coef[3]
  int.right.hi.mu <- sum.right.hi$coef[1]
  int.right.hi.se <- sum.right.hi$coef[3]
  
  sharp.left.mu <- abs(int.left.lo.mu - int.left.hi.mu)
  sharp.left.se <- sharp.left.mu * sqrt(
    (int.left.lo.se/int.left.lo.mu)^2 +
      (int.left.hi.se/int.left.hi.mu)^2)
  
  sharp.right.mu <- abs(int.right.lo.mu - int.right.hi.mu)
  sharp.right.se <- sharp.right.mu * sqrt(
    (int.right.lo.se/int.right.lo.mu)^2 +
      (int.right.hi.se/int.right.hi.mu)^2)
  
  sharpness <- round(c(sharp.left.mu, sharp.left.se,
                       sharp.right.mu, sharp.right.se),
                     iDigits)
  names(sharpness) <- c("left.sharp.mu",  "left.sharp.se",
                        "right.sharp.mu", "right.sharp.se")
  
  raggedness <- round(c(left.fit.mean.sq.resid,
                        right.fit.mean.sq.resid), iDigits)
  names(raggedness) <- c("left raggedness", "right raggedness")
  
  
  line.width <- round(c(line.width.mu, line.width.se), iDigits)
  names(line.width ) <- c("Estimate", "Std. Error")
  
  
  res <- list(name=name, line.width=line.width,
              raggedness=raggedness, sharpness=sharpness)
  
  res
  
}
