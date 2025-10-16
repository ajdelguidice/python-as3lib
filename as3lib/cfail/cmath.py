def itk_windowcalculate(neww: float, newh: float, startw: int, starth: int):
   xmult = neww / startw
   ymult = newh / starth
   return ymult if xmult > ymult else xmult


def itk_windowresizefont(fo: int, mu: float):
   return round((fo * mu) / 100)


def multdivide(number, multiplier, diviser):
   return number * multiplier / diviser


def roundedmultdivide(number, multiplier, diviser):
   return round(number * multiplier) / diviser
