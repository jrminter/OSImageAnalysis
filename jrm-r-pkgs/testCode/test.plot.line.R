# test.plot.line.R

rm(list=ls())
setwd("~/git/jrm-r-pkgs/testCode/")

require(measureLines)

str.file <- './qm-03860-IAM1-BX60-ifs-001.csv'
n.files <- 1
iDigits <- 3
the.name <- "qm-03860-IAM1-BX60"

raw.dat <- read.table(file=str.file, sep=',',
                      header=TRUE, as.is=TRUE)


linewidthplot(raw.dat, 2, the.name)

str.pdf <-paste0('./', the.name,"-lw.pdf")
pdf.options(useDingbats=TRUE)
dev.copy2pdf(file="temp.pdf", width=9,
             height=6, pointsize=12)
embedFonts("temp.pdf","pdfwrite", str.pdf)
unlink("temp.pdf")
