# proc.report.dir.R
require(jrmmisc)
proc.report.dir <- function(path, n.term.dig=3L, iDigits=5){
  csv.files <- list.files(path=path, pattern=".csv")
  n.files <- length(csv.files)
  # print(n.files)
  df.sum <-data.frame( obs=vector(mode="numeric", length=n.files),
                       lw.mu=vector(mode="numeric", length=n.files),
                       lw.se=vector(mode="numeric", length=n.files),
                       rag.r=vector(mode="numeric", length=n.files),
                       rag.l=vector(mode="numeric", length=n.files),
                       sh.r.mu=vector(mode="numeric", length=n.files),
                       sh.r.se=vector(mode="numeric", length=n.files),
                       sh.l.mu=vector(mode="numeric", length=n.files),
                       sh.l.se=vector(mode="numeric", length=n.files))
  for(f in csv.files){
    x <- strsplit(f, ".csv")
    y <- nchar(x)
    z <- substr(x, y-(n.term.dig-1), y)
    z <- as.numeric(z)
    str.file <- paste0(path, f)
    df.sum$obs[z]=z
    str.roi <- sprintf("roi-%d",z)
    raw.dat <- read.table(file=str.file, sep=',', header=TRUE,
                          as.is=TRUE)
    res <- analyze.line.segment(str.roi, raw.dat, iDigits)
    df.sum$lw.mu[z] <- res$line.width[1]
    df.sum$lw.se[z] <- res$line.width[2]
    df.sum$rag.r[z] <- res$raggedness[2]
    df.sum$rag.l[z] <- res$raggedness[1]
    df.sum$sh.r.mu[z] <- res$sharpness[3]
    df.sum$sh.r.se[z] <- res$sharpness[4]
    df.sum$sh.l.mu[z] <- res$sharpness[1]
    df.sum$sh.l.se[z] <- res$sharpness[2] 
  }
  # print(df.sum)
  
  res.med <- sapply(df.sum[,-1], median)
  res.iqr <- sapply(df.sum[,-1], IQR)
  res.mu  <- sapply(df.sum[,-1], mean)
  res.sd  <- sapply(df.sum[,-1], sd)
  res.lcl <- sapply(df.sum[,-1], v.l.cl)
  res.ucl <- sapply(df.sum[,-1], v.u.cl)
  cnt <- rep(n.files,6)
  
  res <- rbind(res.med, res.iqr, res.mu, res.sd, res.lcl, res.ucl)
  res <- round(res, iDigits)
  row.names(res) <- c("median", "iqr", "mean", "std dev",
                      "mean.lcl", "mean.ucl")
  # no need to keep s.e. estimates...
  res <- res[, -c(2,6,8)]
  res
}