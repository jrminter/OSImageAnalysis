#' Contour plot for Ni/Cu K-Ratio RMS-deviation
#' 
#' Prepare a contour plot from a data frame containing the RMS deviation
#' Ni and Cu K-ratios from model values as a function of Ni and Cu thickness. 
#'
#' @param data A data frame with tNi, tCu, and RMSdev values \code{data}
#' @param lab.cex Optional size for label \code{lab.cex}
#' @param icp Optional string with ICP values \code{icp}
#' @param pdf Optional string with path for a PDF of the plot\code{pdf}
#'
#' @return A plot
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' 
ni.cu.rmsdev.contour.plot <- function(data, lab.cex=0.9, icp="", pdf=""){
  oldPar <- par(c('mar','plt','pin','xaxs','yaxs'))
  
  data <- data[with(data, order(tNi, tCu)), ]
  rs <- acast(data, tCu~tNi, value.var="rmsDev")
  y <- as.numeric(colnames(rs))
  x <- as.numeric(rownames(rs))
  df2 <- data[with(data, order(rmsDev)), ]
  
  #             B    L    T    R
  std.mar <- c(5.1, 4.1, 4.1, 2.1)
  plt.mar <- c(5.1, 4.1, 0.5, 0.5)
  par(mar=plt.mar)
  
  # use method from TeachingDemos squishplot to get an aspect ratio of 1
  y.min <- min(y)
  y.max <- max(y)
  ylim <- c(y.min, y.max)
  
  x.min <- min(x)
  x.max <- max(x)
  xlim <- c(x.min, x.max)
  
  if( oldPar$xaxs == 'i' ){ # not extended axis range
    xlim <- range(xlim, na.rm=TRUE)
  } else { # extended range
    tmp.r <- diff(range(xlim, na.rm=TRUE))
    xlim <- range(xlim, na.rm=TRUE) + c(-1,1)*0.04*tmp.r
  }
  
  if( oldPar$yaxs == 'i' ){ # not extended axis range
    ylim <- range(ylim, na.rm=TRUE)
  } else { # extended range
    tmp.r <- diff(range(ylim, na.rm=TRUE))
    ylim <- range(ylim, na.rm=TRUE) + c(-1,1)*0.04*tmp.r
  }
  
  
  tmp2 <- (ylim[2]-ylim[1])/(xlim[2]-xlim[1])
  
  tmp.y <- oldPar$pin[1] * tmp2
  
  if(tmp.y < oldPar$pin[2]){ # squish vertically
    par(pin=c(oldPar$pin[1], tmp.y))
    par(plt=c(oldPar$plt[1:2], par('plt')[3:4]))
  } else { # squish horizontally
    tmp.x <- oldPar$pin[2]/tmp2
    par(pin=c(tmp.x, oldPar$pin[2]))
    par(plt=c(par('plt')[1:2], oldPar$plt[3:4]))
  }
  
  contour(x,y,rs,
          xlab='Cu thickness [nm]',
          ylab='Ni thickness [nm]')
  minCu <- df2$tCu[1]
  minNi <- df2$tNi[1]
  abline(v=minCu, col='red')
  abline(h=minNi, col='red')
  labMC  <- sprintf("Min: %d nm Ni, %d nm Cu", minNi, minCu )
  mtext(labMC, side=1, line=2, adj=1.0, cex=lab.cex, col="red")
  l=nchar(icp)
  if(l>1){
    # add the icp data
    mtext(icp, side=1, line=2, adj=0.0, cex=lab.cex, col="blue")
  }
  l=nchar(pdf)
  if(l>1){
    # now for the pdf
    d.cur <- dev.cur()
    dev.copy2pdf(device=d.cur, file="temp.pdf", useDingbats=TRUE, pointsize=12)
    str.cmd <- sprintf("pdfcrop --margins 10 temp.pdf %s", pdf)
    system(str.cmd)
    unlink("temp.pdf")
  }
  par(oldPar)
}