open("C:\\Users\\jrminter\\Documents\\git\\OSImageAnalysis\\images\\George.tif");
run("Find Edges");
run("Skeletonize (2D/3D)");
run("Find Connected Regions", "allow_diagonal display_one_image display_results regions_for_values_over=100 minimum_number_of_points=1 stop_after=-1");
run("Save XY Coordinates...", "background=0 save=C:\\Users\\jrminter\\Documents\\git\\OSImageAnalysis\\images\\George.txt");
run("Close All");
