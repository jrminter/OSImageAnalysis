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

from ij import IJ, ImagePlus, WindowManager
#import random # a python library for pseudorandom numbers. java.util.Random could be used as well. Jython probably uses that anyway.
from java.util import Random

# get the current image
imp = WindowManager.getCurrentImage()
# check that its a valid image!
if None == imp:
	IJ.showMessage("No images open!")
else:
	# grab its processor and make a ByteProcessor out of it
	ip = imp.getProcessor().crop()
	ip = ip.convertToByte(0)
	pixels = ip.getPixels() # this returns a java.lang.Object, but it is magically usable as the byte[] that it actually is! Good for python!
	# add random noise to its pixels
	r = Random()
	i = 0
	for p in pixels:
	#for i in range(0, len(pixels)): # no significant speed up
		# p is a byte and ranges from -128 to 127
		pix = p #pixels[i]
		if pix < 0: pix = 256 - pix # now pixels are in 0-255
		#rand = pix + random.randint(-128, 127) # 44 seconds for 600x900 8-bit
		rand = pix + r.nextInt(256) - 128 # 16 seconds for 600x900 8-bitusing the java side: about 40% of the python time!
		if rand > 255: rand = 255
		if rand < 0: rand = 0
		if rand > 127: rand = rand - 256 # back to -128 to -1
		pixels[i] = rand # p = rand  results in no changes, because p is a copy
		i +=1
	#ip.setPixels(pixels) # not needed
	ip.resetMinAndMax()
	# show it in a new image
	ImagePlus("Noisy", ip).show()
"""
The byte array in ip.getPixels() is odd:
	from 0 to 127 is 0-127 in integer 0-255 space
	from -128 to -1 is 128-255 in integer 0-255 space
"""

