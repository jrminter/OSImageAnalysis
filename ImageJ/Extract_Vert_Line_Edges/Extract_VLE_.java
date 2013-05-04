import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

public class Extract_VLE_ implements PlugInFilter {
  public int setup(String arg, ImagePlus im) {
    return DOES_32; // this plugin accepts 32-bit grayscale images 
  }
  
  public void run(ImageProcessor ip) {
  	boolean bBkgLight=true;
  	double dDeltaFrac = 0.5;
    double dBkgWidthFrac = 0.15;
    double dLineWidthFrac = 0.15;

    double dMeanGrayL = 52741.;
    double dMeanGrayR = 52962.;
    double dMeanGrayLine = 11184.;
    double dMeanGrayBkg = 0.5*(dMeanGrayL+dMeanGrayR);
    double dDeltaGray = 
    int w = ip.getWidth();
    int h = ip.getHeight();
  }
}