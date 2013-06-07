string unitstring, imgname, imgdesc
image imFront, imInt
number sizex, sizey, scalex, scaley, bDescr, lDesc

imFront := GetFrontImage();
TagGroup tgSrcParams = ImageGetTagGroup(imFront)
getname(imFront, imgname);
getsize(imFront, sizex, sizey);
imgdesc = ImageGetDescriptionText(imFront)
bDescr=StringIsValid(imgdesc)
imFront = max(imFront,0);
imFront = min(imFront,65535);
imInt := IntegerImage("Int", 2,0, sizex, sizey)
TagGroup tgDstParams = ImageGetTagGroup(imInt)
imInt = imFront
getscale(imFront, scalex, scaley)
getunitstring(imFront, unitstring)
setscale(imInt, scalex, scaley)
setunitstring(imInt, unitstring)
taggroupcopytagsfrom(tgDstParams, tgSrcParams)
if (bDescr) {
   ImageSetDescriptionText(imInt, imgdesc)
}
deleteimage(imFront)
imagesetname(imInt, imgname)
showImage(imInt)
