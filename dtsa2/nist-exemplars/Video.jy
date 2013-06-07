import dtsa2
import dtsa2.mcSimulate3 as mc3

def video(e0 = 20.0, nTraj = 200, dim = 2.0e-6, size = 512, name = "video", buildSample = mc3.buildBulk, buildParams = { "Material": material("Cu") }, xtraParams = {}):
   """video(e0 = 20.0, nTraj = 100, dim = 1.0e-5, size = 512, name = "video", buildSample = buildBulk, buildParams = { "Material" : material("Cu" }, xtraParams = {}) represents a generic mechanism for generating frame to make a movie showing electron trajectories."""
   if e0 < 0.1:
      raise "The beam energy must be larger than 0.1 keV."
   if nTraj < 1:
      raise "The number of electron trajectories must be larger than or equal to 1."
   name = name.strip()
   # Place the sample at the optimal location for the detector
   origin = ( 0.0, 0.0, 0.0 )
   # Create a simulator and initialize it
   monte = nm.MonteCarloSS()
   monte.setBeamEnergy(epq.ToSI.keV(e0))
   buildSample(monte, origin, buildParams)
   # Add event listeners to model characteristic radiation
   ti = nm.TrajectoryImage(size, size, dim)
   ti.setXRange(origin[0] - 0.5 * dim, origin[0] + 0.5 * dim)
   ti.setYRange(origin[2] - 0.1 * dim, origin[2] + 0.9 * dim)
   ti.setMaxTrajectories(nTraj)
   monte.addActionListener(ti)
   defOut = (dtsa2.DefaultOutput if dtsa2.DefaultOutput else dtsa2.reportPath())+"/"+name
   jio.File(defOut).mkdirs()
   print defOut
   j=0
   tf=textFile(defOut+"/imgs.txt")
   bf=textFile(defOut+"/compose.bat")
   cx=20
   for i in xrange(0, nTraj):
      monte.runTrajectory()
      fn="tmp%d.png" % (i)
      ti.dump(jio.File(defOut,fn))
      ti.clear(True)
      tf.println("frame%d.png" % i)
      bf.println("copy background.png tmp.png")
      for j in range((i-cx if i-cx>=0 else 0),i+1):
         bf.println("composite -dissolve %d tmp%d.png tmp.png tmp.png" % ((100*((cx+1) - (i-j)))/(cx+1),j))
      bf.println("copy tmp.png frame%d.png" % i)
   bf.println("copy background.png tmp.png")
   for j in xrange(0,nTraj):
      bf.println("composite -dissolve 100 tmp%d.png tmp.png tmp.png" % j)
   bf.println("copy tmp.png frame%d.png" % nTraj)
   tf.println("frame%d.png" % nTraj)
   bf.println('convert -delay 10 -loop 1 @imgs.txt "%s.gif"' % name)
   bf.println("del tmp.png")
   bf.close()
   tf.close()

def buildSphere(monte, origin, buildParams):
   radius = buildParams["Radius"]
   subMat = buildParams["Substrate"]
   mat = buildParams["Material"]
   sphere = nm.Sphere(epu.Math2.plus(origin, [0.0, 0.0, radius]), radius)
   monte.addSubRegion(monte.getChamber(), mat, sphere)
   if subMat:
      monte.addSubRegion(monte.getChamber(), subMat, nm.MultiPlaneShape.createSubstrate([0.0, 0.0, -1.0], epu.Math2.plus(origin, [0.0, 0.0, 2.0 * radius])))
   
video(e0=25, dim = 3.0e-6, name= "K411 sphere 0_7 um at 25 keV", buildSample=buildSphere, buildParams = { "Radius" : 0.7e-6, "Substrate" : material("C",1.9), "Material" : material("K411") })

video(e0=20, dim = 3.0e-6, name= "K411 sphere 0_7 um at 20 keV", buildSample=buildSphere, buildParams = { "Radius" : 0.7e-6, "Substrate" : material("C",1.9), "Material" : material("K411") })

video(e0=15, dim = 3.0e-6, name= "K411 sphere 0_7 um at 15 keV", buildSample=buildSphere, buildParams = { "Radius" : 0.7e-6, "Substrate" : material("C",1.9), "Material" : material("K411") })

video(e0=10, dim = 3.0e-6, name= "K411 sphere 0_7 um at 10 keV", buildSample=buildSphere, buildParams = { "Radius" : 0.7e-6, "Substrate" : material("C",1.9), "Material" : material("K411") })

video(e0=5, dim = 3.0e-6, name= "K411 sphere 0_7 um at 5 keV", buildSample=buildSphere, buildParams = { "Radius" : 0.7e-6, "Substrate" : material("C",1.9), "Material" : material("K411") })