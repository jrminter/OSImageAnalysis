import ij.*;
import ij.process.*;
import ij.gui.*;
import java.awt.*;
import ij.plugin.*;

public class My_Plugin implements PlugIn {

        public void run(String arg) {
                ImagePlus imp = IJ.getImage();
                imp2 = imp.duplicate();
                //IJ.setTool("oval");
                imp.setRoi(new OvalRoi(203,34,172,377));
                imp.setRoi(new OvalRoi(40,34,335,377));
                imp.setRoi(new OvalRoi(40,34,374,377));
                imp.setRoi(new OvalRoi(40,34,374,389));
                IJ.setAutoThreshold(imp, "Default");
                Prefs.blackBackground = false;
                IJ.run(imp, "Convert to Mask", "");
                IJ.run("Close");
                IJ.run("Set Measurements...", "area mean integrated add redirect=colony.jpg decimal=3");
                IJ.run(imp, "Analyze Particles...", "  show=Outlines display exclude summarize");
        }

}
