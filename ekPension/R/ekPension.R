# source("/Users/jrminter/git/OSImageAnalysis/ekPension/R/ekPension.R")
# source("M:/work/Sweave/ekPension/R/ekPension.R")

rm(list=ls())

setwd("/Users/jrminter/git/OSImageAnalysis/ekPension/R")
# setwd("M:/work/Sweave/ekPension/R")
strInFile <- "../dat/us_krip.csv"
strOutPng <- "../out/us_krip.png"
strOutPdf <- "../out/us_krip.pdf"

raw.data <- read.csv(file=strInFile, head=TRUE, sep=",", as.is=TRUE)
print(names(raw.data))
class(raw.data$Date)

# let's make a vector of fractional years using
# R's Date and POSIXlt classes
lData <- length(raw.data$Date)
x <- vector(mode="numeric",length=lData)
for(i in 1:lData)
{
   a.dt <- as.Date(raw.data$Date[i], format='%Y-%m-%d')
   p.dt <- as.POSIXlt(a.dt)
   y.fr <- (p.dt$yday + 1) / 365
   yr <- p.dt$year + 1900 + y.fr
   x[i] <- yr
}
y <- raw.data$Krip.Funding

krip.lr <- lm(y~x)
print(summary(krip.lr))

dummy.x <- seq(2008,2014,1)
nPts <- length(dummy.x)
dummy.y <- vector(mode='numeric',length=nPts)
dummy.y[1:2] <- 0.0
dummy.y[3:nPts] <- max(y)

conf.frame <- data.frame(x=dummy.x)
krip.conf <- predict(krip.lr, interval="conf", newdata = conf.frame)
krip.pred <- predict(krip.lr, interval="pred", newdata = conf.frame)

plot_pension <- function(v.cex=1.2, a.cex=1.2, p.cex=1.1, t.cex=1.2, st.cex=1.1, l.cex=1, lw.fit=3, lw.ax=3, lw.pts=2)
{
  plot(dummy.x, dummy.y, type="n", xlab="", ylab="", axes=FALSE) # setting up coord. system
  points(x, y, pch=21, lwd=lw.pts, cex=p.cex)   
  matlines(conf.frame$x, krip.conf, lty=c(1,2,2), lwd=lw.fit, col=c("black","red","red"))
  matlines(conf.frame$x, krip.pred, lty=c(1,4,4), lwd=lw.fit, col=c("black","blue","blue"))
  # draw an axis on the bottom
  axis(1, cex.axis=a.cex, lwd=lw.ax)
  # draw an axis on the left
  axis(2, cex.axis=a.cex, lwd=lw.ax)
  # draw a box around the plot
  box(lwd=lw.ax)
  mtext("Year", side=1, line=2, cex=v.cex)
  mtext("KRIP Funding", side=2, line=2, cex=v.cex)
  legend("topright",
          inset=.02,
          title="Confidence Intervals",
          c("line", "fit"),
          col=c("red", "blue"),
          lty=c(2,2),
          lwd=c(lw.fit,lw.fit),
          xjust=1, yjust=1, cex=a.cex,
          horiz=FALSE)
}

# first time for the graphics window
plot_pension()

# plot the second time for the png
png(strOutPng, width=800, height=600)
plot_pension(v.cex=1.4, a.cex=1.4)
dev.off()

# plot a third time for the pdf file
pdf(file=strOutPdf, width=9, height=6, pointsize=14)
plot_pension(v.cex=1.2, a.cex=1.2)
dev.off()


b <- krip.lr$coefficients[1]
m <- krip.lr$coefficients[2]
x.int <- -b/m

zero.yr <- trunc(x.int, 0)
zero.mo <- 12*(x.int-zero.yr)
zero.day <- 30*(zero.mo - trunc(zero.mo, 0))
zero.mo <- trunc(zero.mo, 0)
zero.day <- trunc(zero.day, 0)

str.zero <- sprintf("%d-%d-%d", zero.mo, zero.day, zero.yr)

print(str.zero)

