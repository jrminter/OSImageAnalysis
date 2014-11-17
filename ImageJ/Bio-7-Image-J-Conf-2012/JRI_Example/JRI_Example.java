/*
This JRI example produces an Image in ImageJ from random data produced in R.
Please note that you can compile and run this example only once in ImageJ!

Reasons:
JRI can instantiate R only once in a process and R does not support re-inititalization.

Make sure after a compilation that you restart ImageJ!

A second compile leads to a crash of ImageJ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

The binary itself however can be executed several times!

It is recommended to use an IDE for the development which starts and stops a process
if a compilation event occurs!

*/

import ij.*;
import ij.process.*;
import ij.plugin.*;
import org.rosuda.JRI.Rengine;
import org.rosuda.JRI.REXP;

public class JRI_Example implements PlugIn {

	private String args[] = { "--no-save" };
	private String name = "imageMatrix";
	private ImagePlus imp;
	private ImageProcessor ip;
	private static Rengine re = null;

	public void run(String arg) {
		if (re == null) {
			re = new Rengine(args, false, null);

			System.out.println("Rengine created, waiting for R");
			if (!re.waitForR()) {
				System.out.println("Cannot load R");
				return;
			}
		}

		REXP x = re.eval("" + name + "<-matrix(runif(1000000)*2500,1000,1000)");
		double matrix[][] = x.asMatrix();
		ip = new FloatProcessor(matrix.length, matrix[0].length);

		for (int i = 0; i < matrix.length; i++) {

			for (int u = 0; u < matrix[0].length; u++) {

				double value = (matrix[i][u]);
				ip.putPixelValue(i, u, value);

			}
		}
		ip.resetMinAndMax();
		imp = new ImagePlus(name, ip);
		imp.show();
        re.end();
	}

}