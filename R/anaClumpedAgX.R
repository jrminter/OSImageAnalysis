# anaClumpedAgX.R
# Analyze and plot the results from anaClumpedGrains.py
# 2015-01-05  JRM 0.2.10  Worked with image and particle numbers and contrast
# 2015-01-06  JRM 0.2.20  Fixed Contrast

rm(list=ls())
library(analab)
library(rXEDS)

gitDir <- Sys.getenv("GIT_HOME")
wrkDir <- paste0(gitDir,"/OSImageAnalysis/R")
rptDir <- Sys.getenv("RPT_ROOT")

sampleID <- "qm-03966-KJL-031"
do.pdf <- TRUE


csvFil <- paste0(rptDir,"/",sampleID,"/",sampleID,".csv")

setwd(wrkDir)

df <- read.csv(csvFil, header=TRUE, as.is=TRUE)

print(head(df))

n.brks = 250

Sys.sleep(0.1)
pf.circ <- function(){
  linear.distn.panel.plot(df$circ, n.brks, kern.bw="nrd0", distn.lab='circularity')
}
pf.circ()
if(do.pdf){
  pdfFil <- paste0(rptDir,"/",sampleID,"/",sampleID,"-circ.pdf")
  rs.plot.pdf(pf.circ(), pdfFil, width = 9, height = 6, pts = 12)
}


Sys.sleep(0.1)
pf.solid <- function(){
  linear.distn.panel.plot(df$solidity, n.brks, kern.bw="nrd0", distn.lab='solidity')
}
pf.solid()
if(do.pdf){
  pdfFil <- paste0(rptDir,"/",sampleID,"/",sampleID,"-solid.pdf")
  rs.plot.pdf(pf.solid(), pdfFil, width = 9, height = 6, pts = 12)
}



Sys.sleep(0.1)
pf.ar <- function(){
  linear.distn.panel.plot(df$a.r, n.brks, kern.bw="nrd0", distn.lab='aspect ratio')
}
pf.ar()
if(do.pdf){
  pdfFil <- paste0(rptDir,"/",sampleID,"/",sampleID,"-ar.pdf")
  rs.plot.pdf(pf.ar(), pdfFil, width = 9, height = 6, pts = 12)
}


df.sp <- df[df$a.r < 1.17,]
df.sp <- df.sp[df.sp$ecd.nm > 5,]
df.sp <- df.sp[df.sp$circ > 0.85,]

Sys.sleep(0.1)
pf.ecd <- function(){
  linear.distn.panel.plot(df.sp$ecd.nm, n.brks=15, kern.bw="nrd0", distn.lab='ECD [nm]')
}
pf.ecd()
if(do.pdf){
  pdfFil <- paste0(rptDir,"/",sampleID,"/",sampleID,"-ecd.pdf")
  rs.plot.pdf(pf.ecd(), pdfFil, width = 9, height = 6, pts = 12)
}

Sys.sleep(0.1)
pf.spc <- function(){
  linear.distn.panel.plot(df.sp$contrast, n.brks, kern.bw="nrd0", distn.lab='single particle contrast')
}
pf.spc()
if(do.pdf){
  pdfFil <- paste0(rptDir,"/",sampleID,"/",sampleID,"-sp-cont.pdf")
  rs.plot.pdf(pf.spc(), pdfFil, width = 9, height = 6, pts = 12)
}

relC <- df.sp$contrast/df.sp$ecd.nm
Sys.sleep(0.1)
pf.rspc <- function(){
  linear.distn.panel.plot(relC, n.brks, kern.bw="nrd0", distn.lab='contrast/ecd')
}
pf.rspc()
if(do.pdf){
  pdfFil <- paste0(rptDir,"/",sampleID,"/",sampleID,"-rsp-cont.pdf")
  rs.plot.pdf(pf.rspc(), pdfFil, width = 9, height = 6, pts = 12)
}


