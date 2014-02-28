\name{writeNiCuImportSG}
\alias{writeNiCuImportSG}
\title{Write an import file for a StrataGem analysis for NiCu}
\usage{
writeNiCuImportSG(df, sName, tNi, tCu, outDir)
}
\arguments{
  \item{df}{A data frame with mean (col:stat, row:mu) KR
  stats for pdL and CuK \code{df}}

  \item{sName}{A short identifier for the sample
  \code{sName}}

  \item{tNi}{A guess for the Ni thickness in nm \code{tNi}}

  \item{tCu}{A guess for the Cu thickness in nm \code{tCu}}

  \item{outDir}{A directory to receive the SG import file
  \code{outDir}}
}
\value{
none
}
\description{
Read an R data frame containing PD and Ni K-Ratio
statistics and construct a StrataGRM import text file.
}
\examples{
### not run
# setwd("~/work/proj/spcCuNi/R")
# edsDir <- Sys.getenv("EDS_ROOT")
# outPath <- paste0(edsDir,"/StrataGEM/")
# dir.create(outPath, showWarnings = FALSE)
# str.kr.rda <- '../dat/qm-03960-OPM4764-S4-KR-DTSA.RData'
# load(str.kr.rda)
# writeNiCuImportSG(qm.03960.OPM4764.S4.DTSA, "qm-03960-OPM4764-S4", 200, 400, outPath)
}
\keyword{keywords}

