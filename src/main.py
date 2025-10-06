from instrument import Instrument
from measurements import Measurements

sa = Instrument.FSC_init()
pwr = Measurements.powerCW(sa, freq=100, span=20)