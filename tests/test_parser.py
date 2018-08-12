import unittest

from wrk2img import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_wrk_output(self):
        with open("wrk.txt") as file:
            wrk_output = file.read()
        self.assertEqual(type(wrk_output), str)
        parsed = self.parser.parse_wrk_output(wrk_output)
        expected_results = ({
            748868.53: {
                50: 250e-6,
                75: 491e-6,
                90: 700e-6,
                99: 5.8e-3,
            }
        }, "localhost:8080")
        self.assertEqual(parsed, expected_results)


if __name__ == '__main__':
    unittest.main()
