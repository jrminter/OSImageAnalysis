scatter.plot.poly <-
function(x, y, delta=NULL, bErrorBars=FALSE, bReg=FALSE, iReg=2,
                       str.x = "X", str.y="Y", str.title="Plot",
                       v.cex=1.2, a.cex=1.2, t.cex=1.2,
                       lw.fit = 2, lw.pts =2, lw.bars =2, lw.ax = 3,
                       len.bars =0.075)
{
   min.x <- min(x)
   max.x <- max(x)
   min.y <- min(y)
   max.y <- max(y)
   fit <- NULL
   if(bReg)
   {
      if(iReg==1)
      {
         fit <- lm(y ~ x)
      }
      else
      {
         fit <- lm(y ~ poly(x, iReg, raw=TRUE))
      }
      delta.x <- max.x - min.x
      x.fit <- seq(min.x - 0.1*delta.x, max.x + 0.1*delta.x, len = 200)
      y.fit <- predict(fit, data.frame(x=x.fit))
      min.x <- min(min.x,min(x.fit))
      max.x <- max(max.x,max(x.fit)) 
      min.y <- min(min.y,min(y.fit))
      max.y <- max(max.y,max(y.fit)) 
   }
   if(bErrorBars)
   {
      min.y <- min(y-1.96*delta)
      max.y <- max(y+1.96*delta)
   }
   x.temp <- c(min.x, max.x)
   y.temp <- c(min.y, max.y)
   x.t <- c(min.x, max.x)
   y.t <- c(min.y, max.y)
   plot(x.t, y.t, type="n", xlab="", ylab="", axes=FALSE) # setting up coord. system
   points(x, y, lwd=lw.pts, lty=3, pch = 1, col="blue")
   if(bReg)
   {
      lines(x.fit, y.fit,col="red", lwd=lw.fit )
   }
   if(bErrorBars)
   {
       # do the error bars
       arrows(x,y, x, y-1.96*delta, angle=90, code=2, length = len.bars, lwd = lw.bars)
       arrows(x,y, x, y+1.96*delta, angle=90, code=2, length = len.bars, lwd = lw.bars)
   }
   # draw an axis on the bottom
   axis(1,cex.axis=a.cex, lwd=lw.ax)
   # draw an axis on the left
   axis(2,cex.axis=a.cex, lwd=lw.ax)
   # draw a box around the plot
   box(lwd=lw.ax)
   mtext(str.x, side=1, line=2, cex=v.cex)
   mtext(str.y, side=2, line=2, cex=v.cex)
   mtext(str.title, side=3, line=1, cex=t.cex)
   
   fit

}

