//ImageJ macro to format ProbeImage .txt outputs. 

input = getDirectory("Input directory");
output = getDirectory("Output directory");

Dialog.create("Probe Image Processing");
Dialog.addNumber("pixel size in microns", 1);
Dialog.addChoice("Select file type:", newArray(".TXT", ".csv"));    
Dialog.show();
pixelsize = Dialog.getNumber();
suffix = Dialog.getChoice();

//Set the LUT to use for the images, default Cyan Hot
Dialog.create("Probe Image Processing");
Dialog.addChoice("What lookup table (LUT) would you like to use?", newArray("Cyan Hot","16 colors","Fire","Grays","cool","mpl-viridis","Rainbow RGB","Thermal","Yellow Hot"));  
Dialog.show();
LUT = Dialog.getChoice();

//Set whether to manually process brightness/contrast for each map or to run through automatically. Default yes. 
Dialog.create("Probe Image Processing");
Dialog.addChoice("Would you like to process individual images?", newArray("Yes","No"));
Dialog.addCheckbox("Use preset Min/Max values?", false)
Dialog.show();
ProcLUT = Dialog.getChoice();
PresetMinMax = Dialog.getCheckbox
if(ProcLUT == "Yes") {
    setBatchMode(false);
    }
else {
    setBatchMode(true);
    }

if(PresetMinMax == true) {
    ProcLUT = "No";
    }
else ;  
    
//Run processFolder function which in turn calls processFile function   
processFolder(input);

function processFolder(input) {
    list = getFileList(input);
    for (i = 0; i < list.length; i++) {
        if(File.isDirectory(input + list[i]))   //if it's a directory, go to subfolder
            processFolder("" + input + list[i]);
        if(endsWith(list[i], suffix))   //if it's a .txt image, process it
            processFile(input, output, list[i], pixelsize);
        //if it's neither a .txt nor a directory, do nothing
    }
}


function processFile(input, output, file,pixelsize) {

//imports .txt file as text image
run("Text Image... ", "open="+"'"+input+file+"'");

//sets the scale according to the microns per pixel prompt above
run("Set Scale...", "distance=1 known="+pixelsize+" pixel=1 unit=um");
w = getWidth();
h = getHeight();

//add room for calibration bar
w1 = w+100;

//add room for scale bar (h1), plus 10px gap to avoid overlapping the image (h2)
h1 = h+50;
h2 = h+10;

//apply chosen LUT
run(LUT);

//if option to process individual maps, waits for each user to set min and max pixel values before adding scale bar etc
if(ProcLUT == "Yes") {
    run("Brightness/Contrast...");
    title = "Adjust Brightness/Contrast";
    msg = "For each channel and Apply, Press OK to proceed";
    waitForUser(title, msg);
}

else ;

//gives the user the option to add min and max values to maps on a per map basis
if (PresetMinMax == true) {
    Dialog.create("Set Min Value");
    Dialog.addString("Please enter the Min value", 0);
    Dialog.show();
    min = Dialog.getString;
    
    Dialog.create("Set Max Value");
    Dialog.addString("Please enter the Max value", 100);
    Dialog.show();
    max = Dialog.getString;
    }
else {
getMinAndMax(min,max);  // get display range
    }
setMinAndMax(min,max);
    
//set foreground and background colour to black (personal preference - this could be made another option)
setBackgroundColor(0, 0, 0);
setForegroundColor(0, 0, 0);
//increase the image size to make room for scale and calibration bars
run("Canvas Size...", "width="+w1+" height="+h1+" position=Top-Left");
makeRectangle(w, 0, 100, h1);
run("Fill","slice");
makeRectangle(0, h, w1, h1);
run("Fill","slice");
run("Calibration Bar...", "location=[Upper Right] fill=Black label=White number=5 decimal=2 font=12 zoom=1");

//determine scale bar size
scalewidth = d2s((w/2)*pixelsize,0);

//determine the denominator to be used to get a rounded scale bar size e.g. 500um rather than 512
if (pixelsize >= 10) {
    scaledenom = 1000;
    }
else if (pixelsize <=0.2) {
    scaledenom = 10;
    }
else scaledenom = 100;

//round of scale bar to appropriate size
scalewidthR = scaledenom*(round(scalewidth/scaledenom));

//stops the scale bar being bigger than half the image size e.g. a 10um scale bar for a 10um map
if (scalewidthR >= ((w*pixelsize)/2)) {
    scalewidthR2 = scalewidthR/2;
    }
else {
    scalewidthR2 = scalewidthR;
    };

//creates scale bar 
makeRectangle(5,h2,1,1);
run("Scale Bar...", "width="+scalewidthR2+" height=4 font=14 color=White background=None location=[At Selection]");

//name the file and save as a jpeg
name = getTitle;
saveAs("Jpeg", output+name);
}
run ("Close All");