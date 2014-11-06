from colorsys import hsv_to_rgb


def hueDegToRGBCol(hue):
  h = hue / 360.
  [r, g, b] =  hsv_to_rgb(h, 1.0, 1.0)
  ret = [255.0*r, 255.0*g, 255.0*b]
  return ret

hue = 30.0
ret = hueDegToRGBCol(hue)



print(ret)
