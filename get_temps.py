import wmi

mon_wmi = wmi.WMI(namespace=r'root/OpenHardwareMonitor')

class TemperatureRetrivalFailure(Exception): pass

def _get_data(name, type, desc):
    vals = list(mon_wmi.Sensor(name=name, SensorType=type))
    if len(vals) < 1:
        raise TemperatureRetrivalFailure('No " + _desc + found. ')
    elif len(vals) > 1:
        raise TemperatureRetrivalFailure('Multiple " + desc + " found. ')
    return vals[0].Value

def get_gpu_temp():
    """Returns the GPU temperature. """
    return str(_get_data('GPU Core', 'Temperature', 'GPU temp'))


def get_gpu_load():
    """Returns percentage of GPU used. """
    return str(_get_data('GPU Core', 'Load', "GPU Load"))

def get_cpu_load():
    """Returns percentage of CPU used. """
    return str(_get_data('CPU Total', 'Load', 'CPU Load'))

def get_mem_use():
    """Returns percentage of memory used. """
    return str(_get_data('Used Memory', 'Data', 'memory usage'))
