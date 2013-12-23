#' Generate the K-Ratio match error for Ni on Cu using a PAP model
#' 
#' Use GMRFilm to compute the RMS deviation between experimental
#' Ni K-alpha and Cu K-alpha K-Ratios and model values computed
#' using the Phi-Rho-Z model of Pouchou and Pichoir (1991).
#'
#' @param vkV A vector of accelerating voltages (kV) to simulate
#' @param vNiKR A vector of NiLa K-ratios measured at vkV
#' @param vCuKR A vector of CuKa K-ratios measured at vkV
#' @param vNiTh A vector of Ni thickness values (nm) to simulate
#' @param vCuTh A vector of Cu thickness (nm) to simulate
#' @param waitSec time to wait for OS to rename output file
#' @param wrkDir A working directory for the computation
#' 
#' @return A data frame with t.Ni, t.Cu, and rms.dev
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' # qm-03692-DJ2-d1
#' # vkV   <- c(12, 15, 20, 25, 30)
#' # vNiKR <- c(0.0741, 0.0628, 0.0257, 0.0188, 0.0117)
#' # vCuKR <- c(0.9004, 0.8847, 0.7693, 0.5739, 0.4045)
#' # vNiTh <- seq(from=5.0, to=30.0, by=5.0)
#' # vCuTh <- seq(from=500.0, to=550.0, by=5.0)
#' # df <- matchErrorNiCu(vkV, vNiKR, vCuKR, vNiTh, vCuTh, 0.1,  wrkDir="C:/Temp/")

matchErrorNiCu <- function( vkV, vNiKR, vCuKR,
                            vNiTh, vCuTh,
                            waitSec, wrkDir="C:/Temp/"){
  wd <- getwd()
  setwd(wrkDir)
  n.kv <- length(vkV)
  
  # create empty output vectors for dataframe
  v.ni  <- vector(mode = "numeric", length = 0)
  v.cu  <- vector(mode = "numeric", length = 0)
  v.rms <- vector(mode = "numeric", length = 0)
  
  # run the Cu thickness loop
  for(j in 1:length(vCuTh)){
    th.cu <- vCuTh[j]
    for(i in 1:length(vNiTh)){
      th.ni <- vNiTh[i]
      # here is where we do the work
      preClean(wrkDir)
      df <- simNiCuSG(vkV, th.ni, th.cu, 35.0, waitSec, wrkDir, echo=FALSE, clean=TRUE)
      v.k.ni.m <- df$kNiLa
      v.k.cu.m <- df$kCuKa
      del.ni <- vNiKR - v.k.ni.m
      del.NiStq <- del.ni * del.ni
      del.cu <- vCuKR - v.k.cu.m
      del.CuStq <- del.cu * del.cu
      rms.dev <- sum(del.CuStq) + sum(del.NiStq)
      rms.dev <- sqrt(rms.dev)
      rms.dev <- rms.dev/n.kv
      
      v.ni  <- append(v.ni, th.ni)
      v.cu  <- append(v.cu, th.cu)
      v.rms <- append(v.rms, rms.dev)
    }
  }
  
  df <- data.frame(tNi=v.ni, tCu=v.cu, rmsDev=v.rms)
  
  setwd(wd)
  return (df)
}