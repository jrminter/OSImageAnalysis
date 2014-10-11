// run("Image Sequence...", "open=/Users/jrminter/git/OSImageAnalysis/images/map/png sort");
run("Image Sequence...", "open=/Users/jrminter/git/OSImageAnalysis/images/map/tile sort");
// The first slice is C and we want to delete it
// run("Delete Slice");
run("Make Montage...", "columns=3 rows=2 scale=1 first=1 last=6 increment=1 border=0 font=12");

