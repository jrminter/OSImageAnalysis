# calcTableForDM200kV.R
setwd("~/git/OSImageAnalysis/magCalD692/R")

str.file <- "../dat/cm20ut-200kv-mag.csv"

px.size.microns <- 14.0
px.size.nm <- 1000. * px.size.microns

df <- read.csv(str.file, header=T, as.is=TRUE)

df$mag.act <- px.size.nm / df$nm.per.px 





lm.fit <- lm(mag.act ~ mag.ind, data=df)
df$mag.act <- round(df$mag.act, 2)
print(summary(lm.fit))

print(head(df))

write.csv(df, str.file)


