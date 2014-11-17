/*
This example produces a matrix with random numbers in R and creates
a new image in ImageJ from the data which is transferred with the
Rserve library.
 */
import ij.*;
import ij.process.*;
import ij.plugin.*;
import org.rosuda.REngine.REXPMismatchException;
import org.rosuda.REngine.Rserve.RConnection;
import org.rosuda.REngine.Rserve.RserveException;

public class Rserve_Example implements PlugIn {

	public void run(String arg) {
		example();
	}

	public void example() {

		double[][] matrix = null;
		ImagePlus imp;
		ImageProcessor ip;
		String name = "imageMatrix";
		try {
			/*Establish a connection with Rserve!*/
			RConnection c = new RConnection();
			/*Evaluate a R command!*/
			c.eval("" + name + "<-matrix(runif(1000000)*2500,1000,1000)");
			/*Transfer the values to Java!*/
			matrix = c.eval("" + name + "").asDoubleMatrix();
			/*Close the Rserve connection!*/
			c.close();
		} catch (REXPMismatchException e) {

			e.printStackTrace();

		} catch (RserveException e) {

			e.printStackTrace();
		}
		/*Create a new image from the R data in ImageJ!*/
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

	}

}