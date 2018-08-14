import unittest

from wrk2img import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_wrk_output(self):
        expected_results = {
            "wrk": ({
                        748868.53: {
                            50: 250e-6,
                            75: 491e-6,
                            90: 700e-6,
                            99: 5.8e-3,
                        }
                    }, "localhost:8080"),
            "wrk2": ({
                         643.28: {
                             50: 15.25e-3,
                             75: 15.46e-3,
                             90: 15.79e-3,
                             99: 22.67e-3,
                         }
                     }, "127.0.0.1:5000")
        }
        for file_name in ["wrk", "wrk2"]:
            with open(file_name) as file:
                wrk_output = file.read()
            self.assertEqual(type(wrk_output), str)
            parsed = self.parser.parse_wrk_output(wrk_output)
            self.assertEqual(parsed, expected_results[file_name])


if __name__ == '__main__':
    unittest.main()
