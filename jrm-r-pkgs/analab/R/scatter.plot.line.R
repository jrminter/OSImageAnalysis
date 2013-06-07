scatter.plot.line <-
function(x, y, delta=NULL, bErrorBars=FALSE, bReg=FALSE,
                       str.x = "X", str.y="Y", str.title="Plot",
                       v.cex=1.2, a.cex=1.2, t.cex=1.2, st.cex=1.2,
                       lw.fit = 2, lw.pts =2, lw.bars =2, lw.ax = 3,
                       len.bars =0.075, i.digits=4)
{
   min.x <- min(x)
   max.x <- max(x)
   min.y <- min(y)
   max.y <- max(y)
   fit <- NULL
   if(bReg)
   {
      fit <- lm(y ~ x)
      # now let's calculate the adjusted R2
      b <- fit$coefficients[[1]]
      a <- fit$coefficients[[2]]
      s <- summary(fit)
      # get what we want from the fit
      inter.mean    <- s[[4]][1]
      inter.sderr <- s[[4]][3]
      slope.mean    <- s[[4]][2]
      slope.sderr <- s[[4]][4]
      adj.r.sq      <- s[[9]]
      slope.mean  <- round(slope.mean, i.digits)
      slope.sderr <- round(slope.sderr, i.digits)
      inter.mean  <- round(inter.mean, i.digits)
      inter.sderr <- round(inter.sderr, i.digits)
      adj.r.sq    <- round(adj.r.sq, 4)
      
      delta.x <- max.x - min.x
      x.fit <- seq(min.x - 0.1*delta.x, max.x + 0.1*delta.x, len = 200)
      conf.frame <- data.frame(x=x.fit)
      fit.conf <- predict(fit, interval="conf", newdata = conf.frame)
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
      matlines(conf.frame$x, fit.conf, lty=c(1,2,2), lwd=lw.fit, col=c("black","red","red"))
   }
   if(bErrorBars)
   {
       # do the error bars - 95 pct CI
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
   if(bReg)
   {
      # mtext(str.fit, side=1, line=3, cex=0.75*v.cex)
      mtext(substitute(list("(slope","intercept", "adjRsq)") == group("(", list(a%+-%b, c%+-%d, e), ")"),
            list(a=slope.mean, b=slope.sderr, c=inter.mean, d=inter.sderr, e=adj.r.sq)),
            line= .25, cex=st.cex)
   }
   mtext(str.y, side=2, line=2, cex=v.cex)
   mtext(str.title, side=3, line=2.5, cex=t.cex)
   
   fit
}

