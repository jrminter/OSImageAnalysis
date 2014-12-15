dir="C:\\Data\\eds\\Oxford\\QM14-04-04F1-Steele\\reports\\qm-04231-49u003-865-FIB-lo\\qm-04231-49u003-865-FIB-lo-7kV-map2\\work\\";
open(dir+"O-ROI.png");
open(dir+"Cu-ROI.png");
open(dir+"P-ROI.png");
open(dir+"Ag-ROI.png");
open(dir+"Pd-ROI.png");
open(dir+"ROI.png");
run("Images to Stack", "name=Stack title=[] use");
run("Make Montage...", "columns=3 rows=2 scale=1 first=1 last=6 increment=1 border=0 font=12");
