# cache.data.file.R
# 
# This is released under the LGPL license.
#
# A Wrapper function to check to see if a local copy of a file
# exists. and if not, download it from a URL. This version works
# on my Win-XP (32 bit) Win7-x64, and MacBook Pro (x64, Mountain Lion)
# systems. offered as-is. I do respond to constructive suggestions.
# This is not an offer of free tech support or a substitute for a 
# Google search....
#
# file-path: a valid path to where you want
cache.data.file <- function(file.path, url, show.platform=FALSE) {
  Platform <- sessionInfo()$R.version$platform
  if(show.platform) {
    print(Platform)
  }
  if(!file.exists(file.path)){
    str.msg <- paste('downloading', file.path,'from', url)
    print(str.msg)
    if(Platform=="i386-w64-mingw32" | Platform=="x86_64-w64-mingw32" ){
      # its windoze
      setInternet2(TRUE)
      download.file(url, destfile=file.path)   
    } else{
      # use curl for mac
      download.file(url, destfile=file.path, method="curl")
    }
  }
}
