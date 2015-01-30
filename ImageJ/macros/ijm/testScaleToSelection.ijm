// testScaleToSelection.ijm
// Scale to selection w/o expanding window
// example for Wayne Rasband 2015-0129

run("Blobs (25K)");
makeRectangle(113, 70, 37, 30);
// the "alt" causes it not to expand window...
setKeyDown("alt");
run("To Selection");
