"""
A Jython script for ImageJ(C).
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
"""

"""
Note:
	- The ImageProcessor.getPixels() method called on a ByteProcessor returns a java.lang.Object, but it is magically usable as the byte[] that it actually is! Good for python!
	- The byte array in ip.getPixels() is quite odd:
		from 0 to 127 is 0-127 in integer 0-255 space
		from -128 to -1 is 128-255 in integer 0-255 space
"""

from ij import IJ, ImagePlus, WindowManager
from java.util import Random
from jarray import zeros

def addNoise(pixels):
	r = Random()
	i = 0
	for p in pixels:
		if p < 0: p = 256 - p
		rand = p + r.nextInt(256) - 128
		if rand > 255: rand = 255
		if rand < 0: rand = 0
		if rand > 127: rand = rand - 256 # back to -128 to -1
		pixels[i] = rand # can't assign 'rand' to 'p', because 'p' is a copy
		i += 1

def processSlice(ip, type):
	if ImagePlus.GRAY8 == type:
		addNoise(ip.getPixels())
	elif ImagePlus.COLOR_RGB == type:
		length = imp.width * imp.height
		r = zeros(length, 'b')
		g = zeros(length, 'b')
		b = zeros(length, 'b')
		ip.getRGB(r, g, b)
		addNoise(r)
		addNoise(g)
		addNoise(b)
		ip.setRGB(r, g, b)
	else:
		ip = ip.convertToByte(1) # with scaling
		addNoise(ip.getPixels())
	ip.resetMinAndMax()

def run(imp):
	if None == imp:
		IJ.showMessage("No images open!")
		return
	type = imp.getType()
	n_slices = imp.getStackSize()
		
	if 1 == n_slices:
		ip = imp.getProcessor().crop()
		processSlice(ip, type)
		# show result in a new image
		ImagePlus("Noisy_" + imp.title, ip).show()
	else:
		stack1 = imp.getStack()
		roi = imp.getRoi()
		if None == roi:
			width = imp.width
			height = imp.height
		else:
			rect = roi.getBounds()
			width = rect.width
			height = rect.height
		stack2 = ImageStack(width, height)
		for i in range(1, n_slices+1):
			ip = stack1.getProcessor(i)
			# stack processors need the roi to be explicitly set
			if roi: ip.setRoi(rect)
			ip = ip.crop()
			processSlice(ip, type)
			stack2.addSlice(stack1.getSliceLabel(i), ip)
		# show result in a new image
		ImagePlus("Noisy_" + imp.title, stack2).show()

# START PROGRAM:
run(WindowManager.getCurrentImage())
