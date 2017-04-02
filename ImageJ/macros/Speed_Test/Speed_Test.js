  importClass(Packages.ij.IJ);
  importClass(Packages.ij.process.FloatProcessor);
  importClass(Packages.ij.ImagePlus);
  importClass(java.lang.System);
  
  sphere();
  
  // This code runs faster when it is in a function. 
  // The Nashorn JavaScript engine included with
  // Java 8 runs this script 27 times faster, compared
  // with the Rhino JavaScript used with Java 6, when
  // 'size' is set to 2048. Nashorn compiles JavaScript
  // into bytecode, which is JIT compiled into machine code.

  // With size =  4096 0.3 sec in Javascript!
  function sphere() {
     var size = 4096;
     var ip = new FloatProcessor(size,size);
     var t0 = System.currentTimeMillis();
     var x, y, dx, dy, d;
     for (y=0; y<size; y++) {
        for (x=0; x<size; x++) {
           dx=x-size/2;
           dy=y-size/2;
           d = Math.sqrt(dx*dx+dy*dy);
           ip.setf(x,y,-d);
        }
     }
     var time = (System.currentTimeMillis()-t0)/1000+" seconds";
     var img = new ImagePlus(time,ip);
     IJ.run(img,"Red/Green","");
     img.show();
  }
