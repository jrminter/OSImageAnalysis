strImg="qm-04337-KR1532C002-S-355-bez-uhr-bse.tif"
nSecWid=2344
nSecHt=512
yOff=0

selectWindow(strImg);
makeRectangle(0, yOff, nSecWid, nSecHt);
run("Duplicate...", " ");
rename("1");
selectWindow(strImg);
makeRectangle(nSecWid, yOff, nSecWid, nSecHt);
run("Duplicate...", " ");
rename("2");
selectWindow(strImg);
makeRectangle(2*nSecWid, yOff, nSecWid, nSecHt);
run("Duplicate...", " ");
rename("3");
