from pathlib import Path
from typing import Dict

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


class ImageGenerator:
    def generate_and_save_image(self, data: Dict[float, Dict[float, float]], website: str, output: Path):
        figure = self.generate_image(data, website)
        self.save_image(figure, output)

    def generate_image(self, data: Dict[float, Dict[float, float]], website: str) -> Figure:
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(1, 1, 1)
        for label, values in data.items():
            x = list(values.keys())
            y = list(values.values())
            ax.plot(x, y, label=str(label) + " req/s")
        ax.legend()
        ax.set(title="Latency graph for %s" % website,
               xlabel="percentile",
               ylabel="latency")
        return fig

    def save_image(self, figure: Figure, output: Path):
        figure.savefig(str(output.resolve()))
