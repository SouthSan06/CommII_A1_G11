import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block implements a real-valued RF Voltage Controlled Oscillator (VCO).

The block generates a cosine waveform at a fixed carrier frequency (fc), whose
amplitude and phase are controlled by the two input signals.

Operation:
At each sample n, the output is computed as:
    y[n] = A[n] * cos(2*pi*fc*n/samp_rate + Q[n])

where:
- A[n] is the amplitude control signal (first/top input)
- Q[n] is the phase control signal in radians (second input)
- fc is the carrier frequency in Hz
- samp_rate is the sampling rate in samples per second

Inputs:
1) First input (A):
   This input controls the instantaneous amplitude of the output signal.
   It can be a constant value (for fixed amplitude) or a time-varying signal
   (for amplitude modulation).

2) Second input (Q):
   This input controls the instantaneous phase (in radians) of the oscillator.
   It allows phase modulation of the carrier. The signal should be continuous
   to avoid phase discontinuities unless abrupt phase changes are desired.

Output:
- A real-valued RF signal (cosine wave) at frequency fc, with amplitude A[n]
  and phase offset Q[n].

Parameters:
- fc (float): Carrier frequency in Hz. It should be less than half the sampling
  rate to avoid aliasing (fc < samp_rate/2).
- samp_rate (float): Sampling rate in samples per second.

Internal behavior:
- The block keeps track of a running sample index (n_m) to ensure phase
  continuity across consecutive calls to the work() function.

Usage recommendations:
- Ensure that fc is properly chosen according to the sampling theorem.
- Use a smooth phase input (Q) for continuous phase modulation.
- If only a fixed phase is needed, Q can be set to zero.
- For constant amplitude, provide a constant value at input A.
- This block is suitable for generating AM/PM modulated carriers or as a
  building component in RF simulation systems.
"""

    def __init__(self, fc=128000, samp_rate=320000):  
        gr.sync_block.__init__(
            self,
            name='e_RF_VCO_ff',   
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32]
        )
        self.fc = fc
        self.samp_rate = samp_rate
        self.n_m=0

    def work(self, input_items, output_items):
        A=input_items[0]
        Q=input_items[1]
        y=output_items[0]
        N=len(A)
        n=np.linspace(self.n_m,self.n_m+N-1,N)
        self.n_m += N
        y[:]=A*np.cos(2*math.pi*self.fc*n/self.samp_rate+Q)
        return len(output_items[0])


