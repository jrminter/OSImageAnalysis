import ij.*;
import ij.plugin.filter.*;
import ij.process.*;
import ij.gui.*;
import ij.Prefs;
/*
 * ImageJ plug-in to perform image leveling by Local Normalization
 * and be called from a macro. This is closely based upon the
 * Local Normalization plug-in (Version 3-Sep-2011) by:
 * 
 * Daniel Sage
 * Biomedical Imaging Group (BIG)
 * Ecole Polytechnique Federale de Lausanne (EPFL)
 * Lausanne, Switzerland
 * 
 * The Local Normalization plug-in is much more interactive
 * and is preferred to select the appropriate parameters for
 * a given group of images. See:
 * 
 * http://bigwww.epfl.ch/sage/soft/localnormalization/
 * 
 * NOTE: Since the plan is to call this from a macro, only
 * 32 bit float images are supported. The conversion to/from
 * other types is best handled by the macro.
 * 
 * Instead of the full featured dialog implemented by Daniel
 * Sage, this version has a simpler generic dialog that saves
 * the desired choices to the preferences. When called from
 * the macro recorder, the desired parameters are properly
 * transferred.
 * 
 * This simplified modification was developed by:
 * John Minter (jrminter@gmail.com) on 17-Mar-2012
 * 
 * Conditions of use:
 * You may freely use this software for research purposes,
 * but you should not redistribute it without the consent
 * of Daniel Sage (daniel.sage@epfl.ch). In addition, we
 * expect you to include a citation or acknowledgment
 * whenever you present or publish results that are based on it.
 * 
 * Revision History
 *    Date       Version    Comments
 * 17-Mar-2012   0.1.100    Initial prototype.
*/

public class Level_Local_Norm implements PlugInFilter {
	private static double SIGMA1_MIN = 0.1;
	private static double SIGMA1_MAX = 50.0;
	private static double SIGMA2_MIN = 0.1;
	private static double SIGMA2_MAX = 50.0;
	private static double TOLERANCE = 1e-6;
	private static String strVersion = "Level Local Norm v 0.1.100";
	
	private ImagePlus	m_imp;
	
	public int setup(String arg, ImagePlus imp) {
	   // SNAPSHOT: We always need a snapshot, also if not needed for
	   // undo (e.g. in case of a stack).
		// if(imp.getType() != ImagePlus.GRAY32) imp.getProcessor().convertToFloat();
		this.m_imp = imp;
		return IJ.setupDialog(imp, DOES_32 | SNAPSHOT);
	  }
	
	public void run(ImageProcessor ip) {
		if (IJ.versionLessThan("1.26a")) {
			IJ.error("Too old version of ImageJ.");
			return;
		}
		// 1. Retrieve preferred parameters, if available
		double dSigma1 = Prefs.getDouble(".ln.sigma1", 3.0);
		double dSigma2 = Prefs.getDouble(".ln.sigma2", 3.0);
		
		// 2. Prepare the generic dialog
        GenericDialog gd = new GenericDialog(strVersion);
        gd.addNumericField("  sigma1:", dSigma1, 1);
        gd.addNumericField("  sigma2:", dSigma2, 1);
        gd.showDialog();
        if (gd.wasCanceled()) return;
        
        // 3. - Retrieve parameters from the dialog
        //      check, and save the preferences...
        dSigma1 = gd.getNextNumber();
        if( dSigma1 < SIGMA1_MIN ) dSigma1 = SIGMA1_MIN;
        if( dSigma1 > SIGMA1_MAX ) dSigma1 = SIGMA1_MAX;
        
        dSigma2 = gd.getNextNumber();
        if( dSigma2 < SIGMA2_MIN ) dSigma2 = SIGMA2_MIN;
        if( dSigma2 > SIGMA2_MAX ) dSigma2 = SIGMA2_MAX;
        
        Prefs.set("ln.sigma1", dSigma1);
        Prefs.set("ln.sigma2", dSigma2);
        
        // 4. Check that the image is sufficiently large for
        //    the algorithm to make sense..

		int nx = this.m_imp.getWidth();
		int ny = this.m_imp.getHeight();
		
		if (nx <= 3) {
			IJ.error("The width of the image is too small.");
			return;
		}

		if (ny <= 3) {
			IJ.error("The height of the image is  too small.");
			return;
		}
		
		// 5. Get down to business and do the work...
		
		this.m_imp.lockSilently();
		
		float[][] data = new float[nx][ny];
		for(int i=0; i<nx; i++) {
			for(int j=0; j<ny; j++) {
				data[i][j] = ip.getPixelValue(i, j);
			}
		}
		
		float tmp[][] = smoothGaussian(data, dSigma1);
		
		for(int i=0; i<nx; i++) {
			for(int j=0; j<ny; j++) {
				data[i][j] = data[i][j] - tmp[i][j];
				tmp[i][j] = data[i][j];
				tmp[i][j] = tmp[i][j] * tmp[i][j];
			}
		}
		
		float var[][] = smoothGaussian(tmp, dSigma2);
		for(int i=0; i<nx; i++){
			for(int j=0; j<ny; j++) {
				var[i][j] = (float)Math.sqrt(var[i][j]);
				ip.putPixelValue(i, j, data[i][j] / var[i][j]);
			}
		}
		
		this.m_imp.unlock();
		ip.resetMinAndMax();
		this.m_imp.updateAndDraw();
	}
	
	/**
	 * Implements a Gaussian smooth filter with a parameter sigma. Use a IIR
	 * filter
	 * 
	 * Mirror border conditions are applied.
	 * 
	 * N iterations of the symmetrical exponential filter (N=3)
	 * 
	 * N sqrt(N^2 + 2*N*sigma^2) alpha = 1 + ------- + ------------------------
	 * sigma^2 sigma^2
	 * 
	 */
	private float[][] smoothGaussian(float[][] in, double sigma) {
		int nx = in.length;
		int ny = in[0].length;

		float[][] out = new float[nx][ny];

		int N = 3;

		double poles[] = new double[N];

		double s2 = sigma * sigma;
		double alpha = 1.0 + (N / s2) - (Math.sqrt(N * N + 2 * N * s2) / s2);
		poles[0] = poles[1] = poles[2] = alpha;

		double row[] = new double[nx];
		for (int y = 0; y < ny; y++) {
			for(int x=0; x<nx; x++)
				row[x] = in[x][y];
			convolveIIR(row, poles);
			for(int x=0; x<nx; x++)
				out[x][y] = (float)row[x];
		}

		double col[] = new double[ny];
		for (int x = 0; x < nx; x++) {
			for(int y=0; y<ny; y++)
				col[y] = out[x][y];
			convolveIIR(col, poles);
			for(int y=0; y<ny; y++)
				out[x][y] = (float)col[y];
		}

		return out;
	}

	/**
	 * Convolve with with a Infinite Impulse Response filter (IIR)
	 * 
	 * @param signal
	 *            1D input signal, 1D output signal at the end (in-place)
	 * @param poles
	 *            1D array containing the poles of the filter
	 */
	private void convolveIIR(double[] signal, double poles[]) {
		double lambda = 1.0;
		for (int k = 0; k < poles.length; k++) {
			lambda = lambda * (1.0 - poles[k]) * (1.0 - 1.0 / poles[k]);
		}
		for (int n = 0; n < signal.length; n++) {
			signal[n] = signal[n] * lambda;
		}
		for (int k = 0; k < poles.length; k++) {
			signal[0] = getInitialCausalCoefficientMirror(signal, poles[k]);
			for (int n = 1; (n < signal.length); n++) {
				signal[n] = signal[n] + poles[k] * signal[n - 1];
			}
			signal[signal.length - 1] = getInitialAntiCausalCoefficientMirror(signal, poles[k]);
			for (int n = signal.length - 2; (0 <= n); n--) {
				signal[n] = poles[k] * (signal[n + 1] - signal[n]);
			}
		}
	}

	/**
		 */
	private double getInitialAntiCausalCoefficientMirror(double[] c, double z) {
		return ((z * c[c.length - 2] + c[c.length - 1]) * z / (z * z - 1.0));
	}

	/**
		 *
		 */
	private double getInitialCausalCoefficientMirror(double[] c, double z) {
		double z1 = z, zn = Math.pow(z, c.length - 1);
		double sum = c[0] + zn * c[c.length - 1];
		int horizon = c.length;

		if (0.0 < TOLERANCE) {
			horizon = 2 + (int) (Math.log(TOLERANCE) / Math.log(Math.abs(z)));
			horizon = (horizon < c.length) ? (horizon) : (c.length);
		}
		zn = zn * zn;
		for (int n = 1; n < (horizon - 1); n++) {
			zn = zn / z;
			sum = sum + (z1 + zn) * c[n];
			z1 = z1 * z;
		}
		return (sum / (1.0 - Math.pow(z, 2 * c.length - 2)));
	}
}

