import time

class Macros:

    def SetAtt(sa, att):
        sa.write(f"INP:ATT {att}dB")
        return att

    def SetRbw(sa, rbw):
        sa.write(f"SENS:BAND {rbw}kHz")
        return rbw

    def SetVbw(sa, vbw):
        sa.write(f"SENS:VBAND {vbw}kHz")
        return vbw

    def PowerLevel(sa, freq, rbw, vbw, att):
        meas_freq = 0  # MHz
        meas_power = 0  # dBm
        return meas_power, meas_freq
    
    def fsc_preset(sa):
        sa.write("*RST")
        return

    def PeakSearch(sa, freq, span):
        
        # test parameters
        meas_freq = 0  # MHz
        meas_power = 0  # dBm
        # cfg SA to test CW
        sa.write(f"SENS:FREQ:SPAN {span}MHz")
        sa.write(f"SENS:FREQ:CENT {freq}MHz")
        sa.write("INP:ATT:AUTO ON")
        sa.write("DISP:TRAC:Y:ADJ")
        sa.write("INIT:CONT OFF")
        sa.write("CALC:MARK1 ON")
        sa.write("CALC:MARK:COUN ON")
        sa.write("INIT;*WAI")
        sa.write("CALC:MARK1:MAX")
        time.sleep(1)
        meas_freq = 1E-6 * float(sa.query("CALC:MARK:COUN:FREQ?"))
        meas_power = float(sa.query("CALC:MARK1:Y?"))
        print(f"Power at {meas_freq} MHz: {meas_power} dBm")
        return meas_power, meas_freq
    
    def TraceData(sa):
        sa.write("FORM:DATA ASC")
        data_str = sa.query("TRAC:DATA? TRACE1")
        data_points = [float(x) for x in data_str.strip().split(",")]
        return data_points