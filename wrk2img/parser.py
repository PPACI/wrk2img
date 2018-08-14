import re
import sys
from typing import Dict, Tuple


class Parser:
    def __init__(self):
        # TODO: Parse wrk2 output
        self.multiplier_per_unit = {
            "s": 1,
            "ms": 1e-3,
            "us": 1e-6,
            "ns": 1e-9,
        }

    def parse_stdin(self) -> Tuple[Dict[float, Dict[float, float]], str]:
        wrk_ouput = self.read_stdin()
        parsed_wrk_output = self.parse_wrk_output(wrk_ouput)
        return parsed_wrk_output

    def read_stdin(self) -> str:
        return sys.stdin.read()

    def parse_wrk_output(self, wrk_output: str) -> Tuple[Dict[float, Dict[float, float]], str]:
        parsed = {}  # type: Dict[float, Dict[float, float]]
        website = re.search(r"Running \d+s test @ https?://(.+?)[/\n]", wrk_output).group(1)
        req_s = float(re.search(" *Requests/sec: +(\d+\.?\d+)", wrk_output).group(1))
        parsed[req_s] = {}
        # parse latency
        for matches in re.findall(" +(\d{2})% +(\d+\.?\d+)(\w+)", wrk_output):
            percentile, result, unit = matches
            scaled_result = round(float(result) * self.multiplier_per_unit[unit],9)
            parsed[req_s][float(percentile)] = scaled_result
        return parsed, website
