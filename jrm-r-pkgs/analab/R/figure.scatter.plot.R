figure.scatter.plot <-
function(x, y,
         lab.x='x', lab.y='y', lab.cex=1.6,
         ax.cex=1.6, ax.lw=3,
         pts.cex=1.6, pts.lw=2, pts.pch=1, pts.col='blue',
         new.mar=c(4.7,4.7,1.1,1.8),
         fixed.scale = FALSE,
         x.lim=c(0,100), y.lim=c(0,100), ... ) {
  old.mar <- par()$mar 
  par(mar=new.mar)
  
  if (fixed.scale==TRUE){
    x.t <- x.lim
    y.t <- y.lim
    plot(x.t, y.t, type="n", xlab="", ylab="", axes=FALSE) # set up}
  } else {
    x.t <- c(min(x), max(x))
    y.t <- c(min(y), max(y))
    plot(x.t, y.t, type="n", xlab="", ylab="", axes=FALSE) # set up}
    
  }
  points(x, y, lwd=pts.lw, lty=3, pch=pts.pch, cex=pts.cex, col=pts.col)
  # draw an axis on the bottom
  axis(1,cex.axis=ax.cex, lwd=ax.lw)
  # draw an axis on the left
  axis(2,cex.axis=ax.cex, lwd=ax.lw)
  # draw a box around the plot
  box(lwd=ax.lw)
  mtext(lab.x, side=1, line=3, cex=lab.cex)
  mtext(lab.y, side=2, line=3, cex=lab.cex)
  par(mar=old.mar) #reset
}
