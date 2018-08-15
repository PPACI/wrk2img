import unittest
from pathlib import Path

from wrk2img import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_wrk_output(self):
        expected_results = {
            'wrk': ({748868.53: {50: 250e-6, 75: 491e-6, 90: 700e-6, 99: 5.8e-3}}, 'localhost:8080'),
            'localhost': ({643.28: {50: 15.25e-3, 75: 15.46e-3, 90: 15.79e-3, 99: 22.67e-3, }}, '127.0.0.1:5000')
        }
        for example in ['localhost', 'wrk', 'wrk2']:
            path = Path('example').joinpath(example)
            with path.open() as file:
                wrk_output = file.read()
            self.assertEqual(str, type(wrk_output))
            parsed = self.parser.parse_wrk_output(wrk_output)
            if path.stem != 'wrk2':
                self.assertEqual(expected_results[str(path.stem)], parsed)
            else:
                self.assertGreater(len(parsed[0][2000.28]), 20)

    def test_parse_multiple_wrk_output(self):
        path = Path('example').joinpath('wrk_cat')
        with path.open() as file:
            wrk_output = file.read()
        parsed = self.parser.parse_wrk_output(wrk_output)
        self.assertEqual(str, type(wrk_output))
        self.assertEqual(2, len(parsed[0]))
        for i in [1, 2]:
            self.assertIn(i, parsed[0])
            self.assertGreater(len(parsed[0][i]), 20)


if __name__ == '__main__':
    unittest.main()
