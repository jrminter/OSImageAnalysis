#RScript - please enter your code here !
#Load the R library!
library(rJava)

#Initialize Java!
.jinit()

#Add the ImageJ *.jar to the classpath!
.jaddClassPath("C:/Programme/ImageJ/ij.jar")

#Create a new object!
IJ<-.jnew("ij/IJ")

#Open an image!
im<-.jcall(IJ,"Lij/ImagePlus;","openImage","C:/bilder luft/Capture_00001.JPG");

#Show the image!
.jcall(im,,"show");# Call the show method!

#Open an image with another method (slowlier but easier to read using reflection)!
im=IJ$openImage("C:/bilder luft/Capture_00001.JPG");

#Open the image!
im$show()

#Infos about methods!
.jmethods(IJ,"openImage")

#Get a reference to the ImageProcessor class!
ip<-.jcall(im,"Lij/process/ImageProcessor;","getProcessor")

#Get integer values from the ImageProcessor!
intValues <- sapply(.jcall(ip,returnSig="[[I","getIntArray"),.jevalArray)

#Transpose the values for the correct image matrix!
intValues<-t(intValues)

#Plot the values with origin in the upper left!
image(intValues,useRaster=TRUE,ylim=c(1,0))