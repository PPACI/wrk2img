import unittest
from glob import glob
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
        for path in glob('example/mono/wrk/*'):
            path = Path(path)
            with path.open() as file:
                wrk_output = file.read()
            self.assertEqual(str, type(wrk_output))
            parsed = self.parser.parse_wrk_output(wrk_output)
            self.assertEqual(expected_results[path.stem], parsed)

    def test_parse_wrk2_output(self):
        expected_results = {
            'issue1': {'website': '127.0.0.1:8080', 'results': {1996.65: {50.0: 0.001183, 99.9: 0.03074}}},
            'wrk2': {'website': '127.0.0.1:80', 'results': {2000.28: {50.0: 0.006671, 99.9: 0.0123}}},
        }
        for path in glob('example/mono/wrk2/*'):
            path = Path(path)
            with path.open() as file:
                wrk_output = file.read()
            self.assertEqual(str, type(wrk_output))
            results, website = self.parser.parse_wrk_output(wrk_output)
            self.assertEqual(expected_results[path.stem]['website'], website)
            expected_website_results = expected_results[path.stem]
            for req_s, latencies in expected_website_results['results'].items():
                self.assertIn(req_s, results)
                for percentile in [50.0, 99.9]:
                    self.assertEqual(latencies[percentile], results[req_s][percentile])
            self.assertEqual(expected_results[path.stem]['website'], website, "bad website")

    def test_parse_empty_output(self):
        path = Path('tests/example/empty.txt')
        with path.open() as file:
            wrk_output = file.read()
        self.assertEqual(str, type(wrk_output))
        with self.assertRaises(ValueError):
            parsed = self.parser.parse_wrk_output(wrk_output)

    def test_parse_multiple_wrk_output(self):
        path = Path('tests/example/multi').joinpath('wrk_cat')
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
