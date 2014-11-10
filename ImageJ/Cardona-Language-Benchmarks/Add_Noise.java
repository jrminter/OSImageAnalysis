/*
A plugin for ImageJ(C).
Copyright (C) 2005 Albert Cardona.
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation (http://www.gnu.org/licenses/gpl.txt )

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. 

You may contact Albert Cardona at albert at pensament.net, at http://www.pensament.net/java/
*/
/** This is the equivalent to the python script Add_Noise.py
 *  which runs 11x to 14x slower! Java is ~10x faster!
 *  The Add_Noise.txt takes about 4x-5x
 *
 * for 600x900 pixels 8-bit:
 *  java: 1-2s
 *  macro: 12s
 *  jython: 44s
 *
 */
import ij.IJ;
import ij.ImagePlus;
import ij.WindowManager;
import ij.process.ImageProcessor;
import java.util.Random;
import ij.plugin.PlugIn;

public class Add_Noise implements PlugIn {
	
	public void run(String argh) {
		ImagePlus imp = WindowManager.getCurrentImage();
		if (null == imp) {
			IJ.showMessage("No images open!");
		} else {
			ImageProcessor ip = imp.getProcessor().crop();
			ip = ip.convertToByte(false);
			Random random = new Random();
			for (int x=ip.getWidth()-1; x>-1; x--) {
				for (int y=ip.getHeight()-1; y>-1; y--) {
					int pixel = ip.getPixel(x, y);
					int rand = pixel + random.nextInt(256) - 128;
					if (rand > 255) rand = 255;
					if (rand < 0) rand = 0;
					ip.putPixel(x, y, rand);
				}
			}
			ip.resetMinAndMax();
			new ImagePlus("Noisy", ip).show();
		}
	}
}
