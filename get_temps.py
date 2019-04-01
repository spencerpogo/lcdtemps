class Temperature:
    """Represents a temperature in celsius. """
    def __init__(self, f=None, c=None):
        if f is None and c is None:
            raise TypeError('Either fahrenheit or celcius should have a value. ')
        elif f is not None and c is not None:
            raise TypeError('Specify a value for eith celsius or fahrenheit, not both. ')
        elif f is not None and c is None:
            self.c = Temperature.f_to_c(float(f))
        elif c is not None and f is None:
            self.c = float(c)
        else:
            raise TypeError('oof f is ' + str(f) + 'c is ' + str(c))

    def get_temp(self):
        return float(self.c)

    def f_to_c(f):
        return (f - 32) * 5.0/9.0

def get_cpu_temp():
    """Returns the CPU temp in celsius. """
    return Temperature(c=5)

def get_gpu_temp():
    """Returns the GPU temp in celsius. """
    return Temperature(f="80")
