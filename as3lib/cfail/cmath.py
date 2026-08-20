def calculate(neww: float, newh: float, startw: int, starth: int):
    xmult = neww / startw
    ymult = newh / starth
    return ymult if xmult > ymult else xmult
