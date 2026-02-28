import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="Diferenciador",
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.prev = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y = output_items[0]

        if len(x) == 0:
            return 0

        y[0] = float(x[0]) - self.prev

        for i in range(1, len(x)):
            y[i] = float(x[i]) - float(x[i-1])

        self.prev = float(x[-1])

        return len(y)
