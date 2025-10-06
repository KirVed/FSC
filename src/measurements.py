import time

class Measurements:

    def powerCW(sa, freq, span):
        
        #test parameters
        meas_freq = 0  # MHz
        meas_power = 0  # dBm

        # set SA to CW mode
        sa.write("*RST")
        sa.write(f"SENS:FREQ:SPAN {span}MHz")
        sa.write(f"SENS:FREQ:CENT {freq}MHz")
        sa.write("INP:ATT:AUTO ON")
        sa.write("DISP:TRAC:Y:ADJ")
        sa.write("INIT:CONT OFF")
        sa.write("CALC:MARK1 ON")
        sa.write("CALC:MARK:COUN ON")
        sa.write("INIT;*WAI")
        sa.write("CALC:MARK1:MAX")
        time.sleep(0.1)
        meas_freq = 1E-6 * float(sa.query("CALC:MARK:COUN:FREQ?"))
        meas_power = sa.query("CALC:MARK1:Y?")
        print(f"Power at {meas_freq} MHz: {meas_power} dBm")
        sa.close()
        return meas_power, meas_freq

