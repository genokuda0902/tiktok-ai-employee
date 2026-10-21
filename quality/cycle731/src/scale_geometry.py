def clamp(x):
    return max(0.0,min(1.0,x))

def smooth(x):
    x=clamp(x)
    return x*x*(3-2*x)

def widths(progress):
    return round(236*smooth(progress/.34)),round(238*smooth((progress-.25)/.40))
