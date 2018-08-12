import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from wrk2img import ImageGenerator


class TestImageGenerator(unittest.TestCase):

    def setUp(self):
        self.image_generator = ImageGenerator()

    def test_generate_image(self):
        data = {}
        image = self.image_generator.generate_image(data)
        self.assertIsNotNone(image)
        # TODO: write some assert
        with TemporaryDirectory(dir='.') as tempdir:
            output = Path(tempdir).joinpath('output.png')
            self.image_generator.save_image(image, output)
            self.assertTrue(output.exists())


if __name__ == '__main__':
    unittest.main()
