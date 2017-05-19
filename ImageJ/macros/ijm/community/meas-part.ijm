// macro from  glyn.nelson@ncl.ac.uk  ImageJ mailing list
// measure particles and save ROI on to original image
//
// 2017-05-19  splits channels...
//
//
// Assumes the image is a MIP'ed tif with PML in channel1, H2AX in
// channel2 (although these can be the other way round and it doesn't
// matter too much except for labelling in results) and DAPI in
// channel3.  It looks for pure overlap and counts respective
// spots.
//
// All results get stored in a concatenating results file.
// Plus the mask images are stored (all 3 original images converted to
// masks plus the coloc maskin the 4th channel)
// so you can see what it did.

var tolerance = 30;
run("Set Measurements...", "area integrated limit display redirect=None
decimal=3");

dir1 = getDirectory("Choose folder with tif files ");
list = getFileList(dir1);

setBatchMode(true);

// create folders for the tifs
dir1parent = File.getParent(dir1);
dir1name = File.getName(dir1);
dir2 = dir1parent+File.separator+dir1name+"_masks";
if (File.exists(dir2)==false) {
    File.makeDirectory(dir2); // new directory for mask images
}

for (i=0; i<list.length; i++) {
    showProgress(i+1, list.length);
    print("processing ... "+i+1+"/"+list.length+"\n     "+list[i]);
    filename = dir1 + list[i];
    if (endsWith(filename, "tif")) {
        path=dir1+list[i];
        run("Bio-Formats Importer", "open="+filename+" autoscale
            color_mode=Default view=Hyperstack stack_order=XYCZT");
        originalImage = getTitle();
        roiManager("Reset");
        selectWindow(originalImage);
        run("Duplicate...", "duplicate channels=1"); //Change this to the DAPI channel slice ******* 
        // run("8-bit");
        setAutoThreshold("Moments dark");
        run("Threshold");
        run("Watershed");
//          run("Entropy Threshold");
        run("Analyze Particles...", "size=120-2500 circularity=0.04-1.00 exclude add");
        rename("nuc");
// nuclei now added to ROI manager

// next find pml bodies
        selectWindow(originalImage);
        run("Duplicate...", "title=PML duplicate channels=3");
//        run("8-bit");
        setAutoThreshold("Triangle dark");
        run("Threshold");
//        rename("PML");

// next find h2ax foci
        selectWindow(originalImage);
        run("Duplicate...", "title=h2ax duplicate channels=2");
        wait(1000);
//        run("8-bit");
        setAutoThreshold("MaxEntropy dark");
        run("Threshold");
//        rename("h2ax");

// Next find colocalised PML-H2AX foci pixels
        imageCalculator("Multiply create", "h2ax","PML");
        selectWindow("Result of h2ax");
        rename(originalImage+":coloc");
        run("Grays");
        for(j=0; j<roiManager("count"); j++) {
            roiManager("select", j);
            run("Find Maxima...", "noise="+tolerance+" output=[Count]");
//            run("Find Maxima...", "noise="+tolerance+" output=[Point Selection]");
            run("Add Selection...");
            }
//        saveAs("Results", dir2+File.separator+originalImage+"_nuc_coloc.xls");

// next find H2AX foci per nuc
        selectWindow("h2ax");
        rename(originalImage+":h2ax");
        for(j=0; j<roiManager("count"); j++) {
            roiManager("select", j);
            run("Find Maxima...", "noise="+tolerance+" output=[Count]");
//            run("Find Maxima...", "noise="+tolerance+" output=[Point Selection]");
            run("Add Selection...");
        }
        // This is saving as it goes along in case it crashes
        saveAs("Results", dir2+File.separator+originalImage + "_nuc_coloc_and_h2ax.xls"); 
        selectWindow(originalImage+"h2ax");
        rename("h2ax");
        selectWindow(originalImage+"coloc");
        rename("coloc");
        selectWindow(originalImage);
        close();

        run("Merge Channels...", "c1=PML c2=h2ax c3=nuc c4=coloc create");
        rename("masks");

        saveAs("TIFF", dir2+File.separator+originalImage+"_colocmasks.tif");


    close();
    }
setBatchMode(false);
}

showMessage("Well, I think we gave them a damn good thrashing there, what what??");

// macro