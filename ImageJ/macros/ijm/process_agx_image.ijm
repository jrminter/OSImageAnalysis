open("/Users/jrminter/Dropbox/datasets/AgX-dat/eia2855ImgSeries/IMAGE027.tif");
run("Properties...", "channels=1 slices=1 frames=1 unit=um pixel_width=0.03143555 pixel_height=0.03144531 voxel_depth=1.0000000");
run("mpl-viridis");
run("Scale Bar...", "width=1 height=6 font=24 color=White background=None location=[Lower Right] bold overlay");
/* run("Canvas Size...", "width=1130 height=768 position=Center-Left"); */
run("Calibration Bar...", "location=[Upper Right] fill=White label=Black number=5 decimal=0 font=12 zoom=1.3 overlay");