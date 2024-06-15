# SDR-BPSK-COMM
A communication system for the Adalm-Pluto SDR utilizing BPSK.

## Overview/Usage
SDR-COMM
- Two SDRs are required
- One SDR must be running the "send" code, while the other runs the "receive" code.
- The SDR that transmits the data will transmit until the correct data is received.

pluto_bpsk:
- One SDR performs both the transmit and receive functions.
- Demonstrates how to transmit and receive data using BPSK.
- First run the "main.py" file to transmit and receive the data, which saves it to a file. Then run "process.py" to view the demodulation.
