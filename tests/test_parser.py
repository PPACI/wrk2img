import unittest

from wrk2img import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_wrk_output(self):
        with open("wrk.txt") as file:
            wrk_output = file.readlines()
        self.assertEqual(type(wrk_output), list)
        parsed = self.parser.parse_wrk_output(wrk_output)
        expected_results = {
            "50": 250e-6,
            "75": 491e-6,
            "90": 700e-6,
            "99": 5.8e-3,
            "req/s": 748868.53,
            "trans/s": 606.33e6
        }
        self.assertEqual(parsed, expected_results)


if __name__ == '__main__':
    unittest.main()
