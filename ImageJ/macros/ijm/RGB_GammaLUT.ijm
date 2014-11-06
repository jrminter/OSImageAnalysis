//ImageJ macro for setting a gamma adjusted look up table
//It is recommended you install this macro via
//either Plugins>Macros>Install... or Strl+Shift+M
//The macro can also be placed in the startup macros folder.

//The macro applies a gamma-adjusted lookup table (LUT)
//The base LUT colour is given by the r, g and b values;
//i.e. use 255, 255, 255 for greys, 255, 0, 0 for red, etc.
//The gamma values range from 0<1 (lighten dark parts of the image)
//to >1 (darken light parts of the image). A gamma of 1
//gives a simple linear LUT.

//Note that the gamma LUT does not modify the image,
//just how it is displayed.
//
// From http://www.richardwheeler.net/contentpages/ImageJ_Macros/RGB_GammaLUT.ijm

var r=255;
var g=255;
var b=255;
var gam=0.8;

macro "RGB Gamma LUT" {
	Dialog.create("RGB Gamma LUT");
		Dialog.addNumber("R", 255, 0, 5, "(0-255)");
		Dialog.addNumber("G", 255, 0, 5, "(0-255)");
		Dialog.addNumber("B", 255, 0, 5, "(0-255)");
		Dialog.addNumber("Gamma", 0.8, 3, 5, "");
	Dialog.show();
		r=round(minOf(maxOf(Dialog.getNumber(), 0), 255));
		g=round(minOf(maxOf(Dialog.getNumber(), 0), 255));
		b=round(minOf(maxOf(Dialog.getNumber(), 0), 255));
		gam=maxOf(Dialog.getNumber(), 0);

	rs=newArray(256);
	gs=newArray(256);
	bs=newArray(256);
	for (i=0; i<256; i++) {
		rs[i]=round(r*pow(i/256, gam));
		gs[i]=round(g*pow(i/256, gam));
		bs[i]=round(b*pow(i/256, gam));
	}
	setLut(rs, gs, bs);
}
