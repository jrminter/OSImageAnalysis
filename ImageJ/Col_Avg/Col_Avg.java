import ij.*;
import ij.plugin.filter.*;

import ij.process.*;

/*
 * ImageJ plug-in to average columns of pixels
 */
public class Col_Avg implements PlugInFilter {
	private static String strVersion = "Col Avg v 0.1.300";
	private ImagePlus	m_ImpOri; // The ImagePlus obj for the original image
	public int setup(String arg, ImagePlus imp) {
		// SNAPSHOT: We always need a snapshot, also if not needed for
		// undo (e.g. in case of a stack).	
		// if(imp.getType() != ImagePlus.GRAY32) imp.getProcessor().convertToFloat();
		this.m_ImpOri = imp;
		
		// we support 8 and 16 bit/px bit grayscale images
		return IJ.setupDialog(imp, DOES_8G | DOES_16 | DOES_32 | SNAPSHOT );
	}
	public void run(ImageProcessor ip) {
		if (IJ.versionLessThan("1.46a")) {
			IJ.error("Too old version of ImageJ.");
			return;
		}
		int iSlices = m_ImpOri.getStackSize();
		if (iSlices > 1) {
			IJ.error("Does not yet support stacks.");
			return;
		}
		
		int iBitDepth = m_ImpOri.getBitDepth();
		if (iBitDepth != 32){
			new ImageConverter(m_ImpOri).convertToGray32();
			ip = m_ImpOri.getProcessor();
		}
		int iW = ip.getWidth();
		int iH = ip.getHeight();
		float[] pix = (float[]) ip.getPixels();
		// loop over pixels and do the column average
		for(int x=0; x<iW; x++){
			float fSum=0.0f, fCount=0.0f, fAvg = 0.0f;
			int iOff=0;
			// compute the column average
			for(int y=0; y<iH; y++){
				iOff=y*iW+x;
				fSum += pix[iOff];
				fCount += 1.0f;
			}
			
			if(fCount > 0) fAvg=fSum/fCount;
			
			// replace the pixels with the column average
			for(int y=0; y<iH; y++){
				iOff=y*iW+x;
				pix[iOff] = fAvg;
			}
		}
		ip.setPixels(pix); // write the corrected intensity
		ip.resetMinAndMax();
		// update 
		m_ImpOri.updateAndDraw();
	}
}