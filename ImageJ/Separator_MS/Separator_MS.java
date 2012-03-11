/*
 * A separator designed by Michael Schmid schmid@iap.tuwien.ac.at in response
 * to a problematic version John Minter jrminter@gmail.com posted on the
 * ImageJ mail list. Some small changed by John Minter...
 * 
 */
import ij.*;
import ij.process.*;
import ij.ImagePlus;
import ij.plugin.filter.*;

public class Separator_MS implements PlugInFilter {
	public int setup(String arg, ImagePlus imp) {
       // Ask to process stacks.
       // SNAPSHOT: We always need a snapshot, also if not needed for
       // undo (e.g. in case of a stack).
       return IJ.setupDialog(imp, DOES_8G | DOES_16 | SNAPSHOT);
   }

   public void run(ImageProcessor ip) {
       int width = ip.getWidth();
       int height = ip.getHeight();
       double maxInt = ip.getMax();
       //don't use old deprecated 'GaussianBlur.blur' method
       // blurGaussian(ImageProcessor ip, double sigmaX, double sigmaY, double accuracy) 
       new GaussianBlur().blurGaussian(ip, 5.0, 5.0, 0.02);
       //for images with foreground = low values:
       // Inverts the image or ROI.
       ip.invert();
       // segmentation lines get value=0 in 'byteLines'
       //   findMaxima(ImageProcessor ip, double tolerance, double threshold, 
       //   int outputType, boolean excludeOnEdges, boolean isEDM) 
       ByteProcessor byteLines = new MaximumFinder().findMaxima(ip, 0.0,
               ImageProcessor.NO_THRESHOLD,
              /* Output type watershed-segmented image */ MaximumFinder.SEGMENTED,
              /*excludeOnEdges=*/ false, 
              /* isEDM */ false);
       // undo Gaussian Blur & invert, restoring original image
       //(we have a snapshot due to the SNAPSHOT flag)
       ip.reset();
       int lineValueInt = (int) maxInt & 0xff;
       if (ip instanceof ShortProcessor) {
    	   lineValueInt = (int) maxInt;
    	   lineValueInt = lineValueInt & 0xffff;
       }
       //or whatever value you want for the lines
       byte[] bPixels = (byte[])byteLines.getPixels();
       for (int y=0, p=0; y<height; y++)   //'p' is pointer in pixels array
           for (int x=0; x<width; x++, p++)
               if (bPixels[p]==0)
                   ip.set(x,y,lineValueInt);
   }

}