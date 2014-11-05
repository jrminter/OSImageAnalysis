/**
* Sinogram computation
* Jean-Christophe Taveau
* http://crazybiocomputing.blogspot.com
* https://gist.github.com/jeesay/3237559
* importClass added by JRM
**/
importClass(Packages.ij.IJ);
importClass(Packages.ij.gui.ProfilePlot);
var nbProj=180;
var step=180/nbProj;
var imp = IJ.getImage();
IJ.run(imp, "8-bit", "");
var stats = imp.getStatistics();
var avg=stats.mean/(stats.max - stats.min) *255;
IJ.log(avg);
IJ.setBackgroundColor(avg,avg,avg);
var out = IJ.createImage("Sinogram", "8-bit Black", imp.getWidth(), nbProj, 1);
var outProc = out.getProcessor();
 
for (var y=0;y<nbProj;y++)
{
  var tmp = imp.duplicate();
  IJ.run(tmp, "Rotate... ", "angle="+(step*y)+" grid=1 interpolation=Bilinear fill");
  tmp.setRoi(0,0,tmp.getWidth(), tmp.getHeight());
  plot = new ProfilePlot(tmp);
  data = plot.getProfile();
  for (var x in data)
    outProc.putPixel(x,y,data[x]);
  tmp.close();
}
out.show();

