#' Write an import file for a StrataGem analysis for NiCu
#' 
#' Read an R data frame containing PD and Ni K-Ratio
#' statistics and construct a StrataGRM import text file.
#'
#' @param df A data frame with mean (col:stat, row:mu) KR stats for pdL and CuK \code{df}
#' @param sName A short identifier for the sample \code{sName}
#' @param tNi A guess for the Ni thickness in nm \code{tNi}
#' @param tCu A guess for the Cu thickness in nm \code{tCu}
#' @param outDir A directory to receive the SG import file \code{outDir} 
#'
#' @return none
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run
#' # setwd("~/work/proj/spcCuNi/R")
#' # edsDir <- Sys.getenv("EDS_ROOT")
#' # outPath <- paste0(edsDir,"/StrataGEM/")
#' # dir.create(outPath, showWarnings = FALSE)
#' # str.kr.rda <- '../dat/qm-03960-OPM4764-S4-KR-DTSA.RData'
#' # load(str.kr.rda)
#' # writeNiCuImportSG(qm.03960.OPM4764.S4.DTSA, "qm-03960-OPM4764-S4", 200, 400, outPath)


writeNiCuImportSG <- function(df, sName, tNi, tCu, outDir){
  prepNiCuKrForSG <- function(df){
    # first just get extract the means
    df <- df[df$stat=='mu', ]
    v.e0 <- df$e0
    v.ni <- df$krNiK
    v.cu <- df$krCuK
    # then reconstruct because I often have many other KRs
    df <- data.frame(e0=v.e0, krNiK=v.ni, krCuK=v.cu)
    df
  }
  krDF <- prepNiCuKrForSG(df)
  l <- nrow(krDF)
  print(l)
  outPath <- paste0(outDir, sName, ".txt")
  print(krDF)
  sink(outPath)
  line <- paste("# STRATAGem Ni/Cu/PET input file for", sName, "\n")
  cat(line)
  cat("$StrataImport_3\n\n")
  cat("# Sample Configuration\n")
  cat("#  Use PAP, fluo. cont., nb max steps 199\n")
  cat("$Comp PAP Conti 199 \n\n")
  cat("# Sample Description \n\n")
  cat("# Ni layer, unknown thickness (A), known concentration\n")
  line <- sprintf("$Layer 8.90 %.1f u\n", 10*tNi)
  cat(line)
  cat("$Elt 28  1.0 k \n\n")
  cat("# Cu layer, unknown thickness (A), known concentration\n")
  line <- sprintf("$Layer 8.96 %.1f u \n", 10*tCu)
  cat(line)
  cat("$Elt 29  1.0 k  \n\n")
  cat("#PET Substrate\n")
  cat("$Layer \n")
  cat("$Elt  6  0.625 k\n")
  cat("$Elt  1  0.042 k\n")
  cat("$Elt  8  0.333 k\n\n")
  cat("# Geometry is optional\n")
  cat("#   Parameters are inconsistent\n")
  cat("#   Takeoff is degrees,\n")
  cat("#   tilt and azimuth are radians\n")
  cat("#   This is 35, 0, 45 degrees...\n")
  cat("$Geom 35.0 0.0 0.7853982 \n\n")
  cat("# Ni measurements Ix/Istd (pure element)\n")
  for(i in 1:l){
    strKV <- sprintf("%.1f", krDF$e0[i])
    line <- paste("$K 28 Ka", strKV, strKV,"\n")
    cat(line)
    strKR <- sprintf("%.5f\n", krDF$krNiK[i])
    cat(strKR)
  }
  cat(" \n")
  cat("# Cu measurements Ix/Istd (pure element)\n")
  for(i in 1:l){
    strKV <- sprintf("%.1f", krDF$e0[i])
    line <- paste("$K 29 Ka", strKV, strKV,"\n")
    cat(line)
    strKR <- sprintf("%.5f\n", krDF$krCuK[i])
    cat(strKR) 
  }
  cat(" \n")
  cat("# End of file \n")
  
  sink()
}
