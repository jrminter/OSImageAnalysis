// Invert the front image
// J.R. Minter
// 2013-05-29

image front := getfrontimage()
number nMax = max(front)
image inv = nMax - front
string name = front.getname() + "-inv"
inv.setname(name)
showimage(inv)
