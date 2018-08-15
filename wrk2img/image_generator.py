from pathlib import Path
from typing import Dict

import matplotlib
from matplotlib.axes import Axes

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


class ImageGenerator:
    def __init__(self, transparent: bool = False, background: str = "FFFFFF"):
        self.transparent = transparent
        self.background = "#" + background

    # TODO: implement background color and transparent option
    def generate_and_save_image(self, data: Dict[float, Dict[float, float]], website: str, output: Path):
        figure = self.generate_image(data, website)
        self.save_image(figure, output)

    def generate_image(self, data: Dict[float, Dict[float, float]], website: str) -> Figure:
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(1, 1, 1)  # type: Axes
        for label, values in data.items():
            x, y = zip(*sorted(values.items()))
            y_ms = [v * 1000 for v in y]
            ax.plot(x, y_ms, label=str(label) + " req/s")
        ax.set_ylim(bottom=max(ax.get_ylim()[0], 0))
        ax.legend()
        ax.set(title="Latency graph for %s" % website,
               xlabel="percentile",
               ylabel="latency [ms]",
               facecolor=self.background)
        return fig

    def save_image(self, figure: Figure, output: Path):
        figure.savefig(str(output), transparent=self.transparent, facecolor=self.background)
