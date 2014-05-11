# nuclei demo from EBImage
library("EBImage")
doDist <- TRUE
nuc <- readImage(system.file('images', 'nuclei.tif', package='EBImage'))
# display(nuc)
nuct <- nuc[,,1]>0.2
nuclabel <- bwlabel(nuct)
cat('Number of nuclei t1 = ', max(nuclabel),'\n')
nuct2 <- thresh(nuc[,,1], w=10, h=10, offset=0.05) 
kern <- makeBrush(5, shape='disc')
nuct2 <- dilate(erode(nuct2, kern), kern)
nuclabel2 <- bwlabel(nuct2)
cat('Number of nuclei t2 = ', max(nuclabel2),'\n')
nucgray <- channel(nuc[,,1], 'rgb')
nuch1 <- paintObjects(nuclabel2, nucgray, col='#ff00ff')
nuclabel3 <- fillHull(nuclabel2)
nuch2 <- paintObjects(nuclabel3, nucgray, col='#ff00ff')
if(doDist){
  display(nuch2)
}
xy = computeFeatures.moment(nuclabel3)[,]
print(xy[1:4,])

sh = computeFeatures.shape(nuclabel3)[,]
print(sh[1:4,])

num=4.0*pi*sh[,1]
den=sh[,2]*sh[,2]

circ=as.data.frame(num/den)
names(circ)="circ"

hist(circ[,1], xlab='circularity', main='nuclei')


