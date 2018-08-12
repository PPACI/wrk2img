from pathlib import Path
from typing import Dict

import matplotlib
from matplotlib.figure import Figure

matplotlib.use("Agg")


class ImageGenerator:
    def generate_and_save_image(self, data: Dict[str, float], output: Path):
        figure = self.generate_image(data)
        self.save_image(figure, output)

    def generate_image(self, data: Dict[str, float]) -> Figure:
        raise NotImplementedError

    def save_image(self, figure: Figure, output: Path):
        raise NotImplementedError
