from instrument import Instrument
from measurements import Measurements

ins = Instrument()          # create an instance
found_ip = ins.fsc_search() # searching FSC IP in network (call instance method; Python passes inst as "self")
sa = Instrument.fsc_init(found_ip) 

#RF tests
Measurements.PowerLevel(sa, freq_start=80, freq_stop=110, freq_step=10, span=1, rbw=1)  # freq in MHz, span in MHz, rbw in kHz
print("Flow completed") 