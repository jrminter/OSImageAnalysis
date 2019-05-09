//
// RandomOvals.ijm
// Wayne Rasband
// Create Random Ovals
// https://imagej.nih.gov/ij/macros/RandomOvals.txt
// 2010-07-29 Downloaded on 2019-05-09 JRM
//
newImage("Untitled", "RGB", 400, 400, 1);
width = getWidth();
height = getHeight();
for (i=0; i<1000; i++) {
    if (nSlices!=1) exit;
    w = random()*width/2+1;
    h = random()*width/2+1;
    x = random()*width-w/2;
    y = random()*height-h/2;
    setForegroundColor(random()*255, random()*255, random()*255);
    makeOval(x, y, w, h);
    run("Fill");
}
img_id = getImageID();
newImage("temp", "RGB", 400, 400, 1);
id_tmp = getImageID();
selectImage(img_id);

outPath = "C:\\Users\\jrminter\\Documents\\git\\OSImageAnalysis\\ImageJ\\output\\random_ovals.png";
saveAs("png", outPath);
close("*");

