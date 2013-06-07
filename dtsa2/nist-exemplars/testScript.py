import dtsa2

# Should return a list of detectors
print dets()

spec1 = simulate("K412",d2,25.0)
spec2 = simulate("K411",d2,25.0)
spec1.display()
spec2.display()
(spec1+spec2).display()
(2.0*spec1).display()
(spec1-spec2).display()
(spec1-spec2).positiveDefinite().display()
(spec1-spec2).abs().display()
print len(spec1)
print "%s and %s" % (spec1, spec2)
print spec1.getCounts(10)
print spec1.getCounts(slice(20,200,2))
print spec1[10]
assert spec1.getChannelWidth()==d2.getChannelWidth()
assert spec1.getZeroOffset()==d2.getZeroOffset()
print spec1.getProperties()
spec1.rename("Test1")
spec2.rename("Test2")
spec1.scale(2.0).display()
assert abs(spec1.maxChannel()-spec2.maxChannel())<2
print spec1.firstNonZeroChannel(), spec1.lastNonZeroChannel()
print spec1.peakIntegral(6260,6590)
spec1.subSample(10.0).display()
specs=spec1.partition(4)
print specs
for spec in specs:
    assert spec.liveTime()==spec1.liveTime()/4.0
