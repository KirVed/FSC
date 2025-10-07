from instrument import Instrument
from measurements import Measurements
import time

ins = Instrument()          # create an instance
found_ip = ins.fsc_search() # searching FSC IP in network (call instance method; Python passes inst as "self")
sa = Instrument.fsc_init(found_ip) 

#RF tests
Measurements.PeakSearch(sa, freq=100, span=20)
#time.sleep(1)
print("Test completed") 