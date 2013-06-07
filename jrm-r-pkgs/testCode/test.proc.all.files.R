# test.proc.all.files.R
rm(list=ls())
setwd("~/git/jrm-r-pkgs/testCode/")
require(measureLines)

data.path <- 'C:/Data/report/qm-03860-IAM1-BX60-ifs/'

res <- proc.report.dir(data.path, 3L)
print(res)





