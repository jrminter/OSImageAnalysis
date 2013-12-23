#' Generate the K-Ratio match error for Pd on Cu using a PAP model
#' 
#' Use GMRFilm to compute the RMS deviation between experimental
#' Pd L-alpha and Cu K-alpha K-Ratios and model values computed
#' using the Phi-Rho-Z model of Pouchou and Pichoir (1991).
#'
#' @param vkV A vector of accelerating voltages (kV) to simulate
#' @param vPdKR A vector of PdLa K-ratios measured at vkV
#' @param vCuKR A vector of CuKa K-ratios measured at vkV
#' @param vPdTh A vector of Pd thickness values (nm) to simulate
#' @param vCuTh A vector of Cu thickness (nm) to simulate
#' @param waitSec time to wait for OS to rename output file
#' @param wrkDir A working directory for the computation
#' 
#' @return A data frame with t.Pd, t.Cu, and rms.dev
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' # vkV   <- c(10, 12, 15, 20, 25, 30)
#' # vPdKR <- c(0.14713, 0.11593, 0.08533, 0.04546, 0.03498, 0.02327)
#' # vCuKR <- c(0.55999, 0.75381, 0.80997, 0.85107, 0.78985, 0.66039)
#' # vPdTh <- seq(from=5.0, to=30.0, by=5.0)
#' # vCuTh <- seq(from=810.0, to=860.0, by=5.0)
#' # df <- matchErrorPdCu(vkV, vPdKR, vCuKR, vPdTh, vCuTh, 0.1,  wrkDir="C:/Temp/")

matchErrorPdCu <- function( vkV, vPdKR, vCuKR,
                            vPdTh, vCuTh,
                            waitSec, wrkDir="C:/Temp/"){
  wd <- getwd()
  setwd(wrkDir)
  n.kv <- length(vkV)
  
  # create empty output vectors for dataframe
  v.pd  <- vector(mode = "numeric", length = 0)
  v.cu  <- vector(mode = "numeric", length = 0)
  v.rms <- vector(mode = "numeric", length = 0)
  
  # run the Cu thickness loop
  for(j in 1:length(vCuTh)){
    th.cu <- vCuTh[j]
    for(i in 1:length(vPdTh)){
      th.pd <- vPdTh[i]
      preClean(wrkDir)
      df <- simPdCuSG(vkV, th.pd, th.cu, 35.0, waitSec, wrkDir, echo=FALSE, clean=TRUE)
      v.k.pd.m <- df$kPdLa
      v.k.cu.m <- df$kCuKa
      del.pd <- vPdKR - v.k.pd.m
      del.PdStq <- del.pd * del.pd
      del.cu <- vCuKR - v.k.cu.m
      del.CuStq <- del.cu * del.cu
      rms.dev <- sum(del.CuStq) + sum(del.PdStq)
      rms.dev <- sqrt(rms.dev)
      rms.dev <- rms.dev/n.kv
      
      v.pd  <- append(v.pd, th.pd)
      v.cu  <- append(v.cu, th.cu)
      v.rms <- append(v.rms, rms.dev)
    }
  }
  
  df <- data.frame(tPd=v.pd, tCu=v.cu, rmsDev=v.rms)
  
  setwd(wd)
  return (df)
}