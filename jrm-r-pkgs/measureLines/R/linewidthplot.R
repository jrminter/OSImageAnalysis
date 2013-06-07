# linewidthplot.R
#
# this function takes a data frame containing the
# left and right edges of line segments produced
# from low, med, or high delta gray thresholds
# and plots the desired line
linewidthplot <- function(dat, thr=2, title="foo",
                      units="microns", iDigits=3){
  if(thr==1){
    # we selected the "low" threshold
    df.left  <- dat[,1:2]
    df.right <- dat[,3:4]
  } else if (thr==2){
    # we selected the "medium" threshold
    df.left  <- dat[,5:6]
    df.right <- dat[,7:8]
    
  } else if (thr==3){
    # we selected the "high" threshold
    df.left  <- dat[,9:10]
    df.right <- dat[,11:12]
    
  } else {
    # an improper threshold selection
    print("Error: theshold must be 1, 2, or 3 for lo, med, or high")
    return(NULL)
  }

  df.left <- df.left[complete.cases(df.left),]
  df.left <- data.frame(l=df.left[,2], t=df.left[,1]) 

  df.right <- df.right[complete.cases(df.right),]
  df.right <- data.frame(l=df.right[,2], t=df.right[,1])
  
  df.left  <- df.left[with(df.left, order(l)), ]
  df.right <- df.right[with(df.right, order(l)), ]  
  
  y.mean.t <- mean(df.right$t)
  y.max.t  <- max(df.right$t)
  y.min.t  <- min(df.right$t)
  y.del.t  <- abs(y.max.t-y.min.t) 
  y.mean.b <- mean(df.left$t)
  y.max.b  <- max(df.left$t)
  y.min.b  <- min(df.left$t)
  y.del.b  <- abs(y.max.b-y.min.b)
  y.del    <- 0.8*(max(y.del.b, y.del.t))
  par(mfrow=c(2,1))
  #             B   L   T   R
  top.mar <- c(0.0,4.1,3.1,2.1)
  bot.mar <- c(5.1,4.1,.1,2.1)
  def.mar <- c(5.1,4.1,3.1,2.1)
  par(mar=top.mar)
  y.lim <- c( y.mean.t-y.del, y.mean.t+y.del)
  plot(df.right$l, df.right$t, type="n", ylim=y.lim, 
       xlab="", ylab="", axes=FALSE)
  lm.fit.r <- lm(df.right$t ~ df.right$l)
  abline(lm.fit.r, col="blue", lwd=3, lty=1)
  points(df.right$l, df.right$t, pch=1, cex=0.7, col="blue")
  axis(2)
  box()
  strY <- paste("width", units)
  mtext(strY , side=2, line=2)
  mtext(title, side=3, line=1)
  par(mar=bot.mar)
  y.lim <- c( y.mean.b-y.del, y.mean.b+y.del)
  plot(df.left$l, df.left$t, type="n", ylim=y.lim,
       xlab="", ylab="", axes=FALSE)
  points(df.left$l, df.left$t, pch=1, cex=0.7, col="red")
  lm.fit.l <- lm(df.left$t ~ df.left$l)
  
  sum.left.fit  <- summary(lm.fit.l)
  sum.right.fit <- summary(lm.fit.r)
  int.right.fit.mu <- sum.right.fit$coef[1]
  int.right.fit.se <- sum.right.fit$coef[3]
  int.left.fit.mu  <- sum.left.fit$coef[1]
  int.left.fit.se  <- sum.left.fit$coef[3]
  line.width.mu <- abs(int.left.fit.mu - int.right.fit.mu)
  line.width.se <- line.width.mu * sqrt(
    (int.left.fit.se/int.left.fit.mu)^2 +
      (int.right.fit.se/int.right.fit.mu)^2)
  line.width.mu <- round(line.width.mu, iDigits)
  line.width.se <- round(line.width.se, iDigits)
  
  legend("topleft", legend = bquote("width:" ~ .(line.width.mu) %+-% .(line.width.se) ~ .(units)))
  
  abline(lm.fit.l, col="red", lwd=3, lty=1)
  axis(2)
  mtext(strY, side=2, line=2)
  strX <- paste("length", units)
  mtext(strX, side=1, line=2)
  axis(1)
  box()
  par(mar=def.mar)
  par(mfrow=c(1,1))
}
