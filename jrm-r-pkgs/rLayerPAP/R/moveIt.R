#' Move the output file for GMRFilm
#'
#' @param wrkDir Working directory for GMRFilm simulation \code{wrkDir}
#'
#' @return none
#'
#' @keywords keywords
#' 
#' @examples
#' ### Not run

moveIt <- function(wrkDir='C:/Temp/'){
  setwd(wrkDir)
  files <- list.files(pattern="^[F]")
  if(length(files) < 1)
  {
    print("error: did not find an output file")
  }
  file.rename(files[1], "./out.txt")
}