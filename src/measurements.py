import time
import os
from macros import Macros

class Measurements:

    @staticmethod
    def PowerLevel(sa, freq_start, freq_stop, freq_step, span, rbw, save_trace = False):  # Power level measure at freq[MHz], span[MHz], rbw[KHz]

        meas_freq = 0  # MHz
        meas_power = 0  # dBm 

        # SA preset
        Macros.fsc_preset(sa)

        # Measurents and logging results to CSV file as a Pivot table (use os.path.join for portability)
        results_dir = os.path.join(r"C:\Users\kiril\VScode\FSCmeas", "results")
        os.makedirs(results_dir, exist_ok=True)
        base_csv = os.path.join(results_dir, "PowerLevel.csv")

        # If base file exists, choose the next available numbered filename: PowerLevel_1.csv, PowerLevel_2.csv, ...
        if not os.path.exists(base_csv):
            csv_path = base_csv
            write_header = True
        else:
            i = 1
            while True:
                candidate = os.path.join(results_dir, f"PowerLevel_{i}.csv")
                if not os.path.exists(candidate):
                    csv_path = candidate
                    write_header = True
                    break
                i += 1

        # Append data; write header only when creating a new file
        with open(csv_path, "a", encoding="utf-8") as f:
            if write_header:
                f.write("Iter,Time,Freq,Span,RBW,Measured Pwr,Measured Freq\n")
            #f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{freq},{span},{rbw},{meas_power},{meas_freq}\n")

        # Test steps 
        j=1
        for freq in range(freq_start, freq_stop + 1, freq_step):
            for span in (1, 10):  # Example spans in MHz
                for rbw in (10, 100):  # Example RBWs in kHz
                    Macros.SetRbw(sa, rbw)                 
                    print(f" Iter:{j}, Measuring at Freq: {freq} MHz, Span: {span} MHz, RBW: {rbw} kHz")
                    res = Macros.PeakSearch(sa, freq, span)
                    meas_power = res[0]
                    meas_freq = res[1]
                    with open(csv_path, "a", encoding="utf-8") as f:
                        f.write(f"{j}, {time.strftime('%Y-%m-%d %H:%M:%S')},{freq},{span},{rbw},{meas_power},{meas_freq}\n")

                    if save_trace:
                        # Read trace data from the analyzer
                        trace_data = Macros.TraceData(sa)

                        # Calculate frequency axis (MHz) for the trace data
                        # delta = span / (n_points - 1)
                        try:
                            n_points = len(trace_data)
                        except Exception:
                            n_points = 0

                        if n_points > 1:
                            delta = span / float(n_points - 1)
                            trace_start_freq = freq - span / 2
                            freq_points = [float(trace_start_freq) + i * delta for i in range(n_points)]
                        elif n_points == 1:
                            freq_points = [float(freq_start)]
                        else:
                            freq_points = []

                        # Save trace (frequency vs power) as a separate CSV per iteration
                        if freq_points and n_points:
                            trace_csv = os.path.join(results_dir, f"PowerLevel_trace_{j}.csv")
                            with open(trace_csv, "w", encoding="utf-8") as tf:
                                tf.write("Freq_MHz,Power_dBm\n")
                                for fx, py in zip(freq_points, trace_data):
                                    tf.write(f"{fx},{py}\n")
                            print(f"Trace saved to {trace_csv}")
                        else:
                            continue

                    time.sleep(0.1)  # slight delay between measurements
                    j+=1

        print(f"Test completed. The results saved to {csv_path}.")