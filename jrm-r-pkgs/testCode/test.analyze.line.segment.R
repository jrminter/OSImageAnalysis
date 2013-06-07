# test.analyze.line.segment.R

rm(list=ls())
setwd("~/git/jrm-r-pkgs/testCode/")
require(measureLines)


str.file <- './qm-03860-IAM1-BX60-ifs-001.csv'
n.files <- 1
iDigits <- 5
the.name <- "IAM1-BX60"

raw.dat <- read.table(file=str.file, sep=',', header=TRUE, as.is=TRUE)

ret <- analyze.line.segment(the.name, raw.dat, iDigits)

print(ret)




