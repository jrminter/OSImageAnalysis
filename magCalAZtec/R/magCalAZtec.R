# magCalAZtec.R
setwd("~/git/OSImageAnalysis/magCalAZtec/R")

str.file <- "../dat/data.csv"

imgWidth <- 1024.

df <- read.csv(str.file, header=T, as.is=TRUE)
df$iMag = 1./df$mag
df$m.per.px <- df$FW.m/imgWidth
# print(head(df))

plot(df$iMag, df$m.per.px)

lm.fit <- lm(m.per.px ~ -1 + iMag, data=df)
sum.lm <- summary(lm.fit)

slope.mu <- sum.lm$coef[1]
slope.se <- sum.lm$coef[2]

print(c(slope.mu, slope.se))


mag <- 50000.

sf.mu.um <- 1.0e9*slope.mu/mag

print(sf.mu.um)

