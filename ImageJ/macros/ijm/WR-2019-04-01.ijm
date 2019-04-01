/* Wayne Rasband 2019-04-01 */
close("*");
setColor("red");
setLineWidth(40);
newImage("Untitled", "rgb black", 507, 446, 1);
drawLine(0,0,507,446);
run("Leaf (36K)");
drawLine(0,0,507,446);
selectImage(1);
drawLine(507,0,0,446);
selectImage(2);
drawLine(507,0,0,446);
run("Tile”);