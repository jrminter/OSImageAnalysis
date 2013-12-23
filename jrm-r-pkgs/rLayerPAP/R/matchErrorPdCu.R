#' Generate the K-Ratio match error for Pd on Cu using a PAP model
#' 
#' Use GMRFilm to compute the RMS deviation between experimental
#' Pd L-alpha and Cu K-alpha K-Ratios and model values computed
#' using the Phi-Rho-Z model of Pouchou and Pichoir (1991).
#'
#' @param vkV A vector of accelerating voltages (kV) to simulate
#' @param vPdKR A vector of PdLa K-ratios measured at vkV
#' @param vCuKR A vector of CuKa K-ratios measured at vkV
#' @param PdLo lowest Pd thickness values (nm) to simulate
#' @param PdHi highest Pd thickness values (nm) to simulate
#' @param PdSt Pd thickness step (nm)
#' @param CuLo lowest Cu thickness (nm) to simulate
#' @param CuHi highest Cu thickness (nm) to simulate
#' @param CuSt Cu thickness (nm) step
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
#'

matchErrorPdCu <- function( vkV, vPdKR, vCuKR,
                            PdLo, PdHi, PdSt,
                            CuLo, CuHi, CuSt,
                            wrkDir="C:/Temp/"){
  wd <- getwd()
  setwd(wrkDir)
  n.kv <- length(vkV)
  preClean(wrkDir)
  # output vectors for dataframe
  v.pd  <- vector(mode = "numeric", length = 0)
  v.cu  <- vector(mode = "numeric", length = 0)
  v.rms <- vector(mode = "numeric", length = 0)
  # run the Cu thickness loop
  th.cu <- CuLo
  while(th.cu < CuHi + CuSt){
    th.pd <- PdLo
    while(th.pd < PdHi + PdSt){
      # here is where we do the work
      df <- simPdCuSG(vkV, th.pd, th.cu, 35.0, wrkDir, clean=TRUE)
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
      
      th.pd <- th.pd + PdSt
    }
    
    th.cu <- th.cu + CuSt
  }
  
  df <- data.frame(tPd=v.pd, tCu=v.cu, rmsDev=v.rms)
  
  setwd(wd)
  return (df)
}