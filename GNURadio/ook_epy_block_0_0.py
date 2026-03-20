import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block implements a complex-envelope (CE) or baseband Voltage Controlled Oscillator (VCO).

The block generates a complex exponential signal whose amplitude and phase are
directly controlled by the two input signals. It produces the complex baseband
representation of a sinusoidal signal.

Operation:
At each sample n, the output is computed as:
    y[n] = A[n] * exp(j * Q[n])

where:
- A[n] is the amplitude control signal (first/top input)
- Q[n] is the phase control signal in radians (second input)
- j is the imaginary unit

Inputs:
1) First input (A):
   This input controls the instantaneous amplitude (magnitude) of the output
   complex signal. It can be constant or time-varying, enabling amplitude
   modulation.

2) Second input (Q):
   This input controls the instantaneous phase in radians. It defines the
   angle of the complex exponential and enables phase or frequency modulation.
   For frequency modulation, Q[n] should be the accumulated phase
   (i.e., the integral of instantaneous frequency).

Output:
- A complex-valued signal (complex64) representing the baseband (complex envelope)
  of a sinusoidal waveform. The real part corresponds to the in-phase (I)
  component and the imaginary part to the quadrature (Q) component.

Parameters:
- This block does not define internal parameters such as carrier frequency or
  sampling rate. These must be implicitly handled by how the phase input Q[n]
  is generated.

Usage recommendations:
- To generate a constant-frequency tone, use:
      Q[n] = 2*pi*f*n/fs
- For frequency modulation (FM), provide Q[n] as the cumulative sum (integral)
  of the desired instantaneous frequency.
- Ensure phase continuity in Q[n] to avoid discontinuities in the output signal.
- If constant amplitude is desired, set A[n] to a fixed value (e.g., 1.0).
- This block is especially useful in baseband simulations, digital modulation
  schemes, and complex signal processing systems."""

    def __init__(self,):  
        gr.sync_block.__init__(
            self,
            name='e_CE_VCO_fc',   
            in_sig=[np.float32, np.float32],
            out_sig=[np.complex64]
        )
        
    def work(self, input_items, output_items):
        A=input_items[0]
        Q=input_items[1]
        y=output_items[0]
        N=len(A)
        y[:]=A*np.exp(1j*Q)
        return len(output_items[0])
