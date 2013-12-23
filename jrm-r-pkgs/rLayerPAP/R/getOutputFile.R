#' Get the output file produced by GMRFilm
#'
#' @return outFile
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run
#' # outFile = getOutputFile()

getOutputFile <- function(){
  files <- list.files(pattern="^[F]")
  if(length(files) < 1)
  {
    print("error: did not find an output file")
    outFile = NA
  }
  outFile <- files[1]
  outFile
}