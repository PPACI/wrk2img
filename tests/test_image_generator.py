import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from wrk2img import ImageGenerator


class TestImageGenerator(unittest.TestCase):

    def setUp(self):
        self.image_generator = ImageGenerator()

    def test_generate_image(self):
        data = {
            748868.53: {
                50: 250e-6,
                75: 491e-6,
                90: 700e-6,
                99: 5.8e-3,
            }
        }
        image = self.image_generator.generate_image(data, "localhost")
        self.assertIsNotNone(image)
        # TODO: write some assert
        with TemporaryDirectory(dir='.') as tempdir:
            output = Path(tempdir).resolve().joinpath('output.png')
            self.image_generator.save_image(image, output)
            self.assertTrue(output.exists())


if __name__ == '__main__':
    unittest.main()
