/*
 * Latex watershed example
 * 
 *   Date          Who      What
 * ----------  -----------  ---------------------------------------------
 * 2019-05-15  John Minter  Initial test
 */
open("D:/Data/images/key-test/pol4455/POL-4455-16bit-Img01-bks.dm3");
run("Median...", "radius=2");
run("Enhance Contrast", "saturated=0.35");
setOption("ScaleConversions", true);
run("8-bit");
run("Gaussian Blur...", "sigma=5");
rename("latex-blur.dm3");
run("Classic Watershed", "input=latex-blur mask=None use min=0 max=134");
// apply LUT to facilitate result visualization
run("3-3-2 RGB");