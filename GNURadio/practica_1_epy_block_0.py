import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='estadistico_total',
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32, np.float32]  # media, varianza, potencia
        )

        self.N = 0
        self.sum_x = 0.0
        self.sum_x2 = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]

        y_media = output_items[0]
        y_var = output_items[1]
        y_pow = output_items[2]

        for i in range(len(x)):
            self.N += 1
            self.sum_x += x[i]
            self.sum_x2 += x[i]**2

            media = self.sum_x / self.N
            potencia = self.sum_x2 / self.N
            varianza = potencia - media**2

            y_media[i] = media
            y_var[i] = varianza
            y_pow[i] = potencia

        return len(x)
