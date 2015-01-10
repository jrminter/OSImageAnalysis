# testImageJfromR.R

# load the library
library(rJava)

# initialize Java
.jinit()

# Add the ImageJ *.jar to the classpath!

strMacIJ <- "/Applications/ImageJ/ImageJ64.app/Contents/Resources/Java/ij.jar"
strMacAT <- "/Applications/ImageJ/plugins/jars/Auto_Threshold.jar"

.jaddClassPath(strMacIJ)
.jaddClassPath(strMacAT)

# Create the IJ object
IJ <- .jnew("ij/IJ")

# strImg <- "/Users/jrminter/dat/images/test/ij/blobs.gif"
strImg <- "http://imagej.net/images/blobs.gif"

# Open the image
imp <- .jcall(IJ,"Lij/ImagePlus;", "openImage", strImg)

w <- .jcall(imp,returnSig="I","getWidth")
h <- .jcall(imp,returnSig="I","getHeight")
shortTitle <- .jcall(imp,returnSig="S","getShortTitle")
print(shortTitle)
print(w)
print(h)

strThrMeth <- "method=Default white"

#.jcall(IJ, returnSig="V", "run", imp, "Threshold", strThrMeth )

ar <- as.numeric(w)/as.numeric(h)

# Get a reference to the ImageProcessor class!
ip <- .jcall(imp,"Lij/process/ImageProcessor;","getProcessor")

# Get integer values from the ImageProcessor!
intValues <- sapply(.jcall(ip,returnSig="[[I","getIntArray"),.jevalArray)


# Transpose the values for the correct image matrix!
intValues <- t(intValues)

# Plot the values with origin in the upper left!
image(intValues, useRaster=TRUE, ylim=c(1,0), bty='n', xaxt='n',
      yaxt='n', asp=ar, col=gray(0:255 / 256))



