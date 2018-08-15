import re
import sys
from enum import Enum
from typing import Dict, Tuple


class RegexLibrary(Enum):
    website = r"Running \d+s test @ https?://(.+?)[/\n]"
    req_s = r" *Requests/sec: +(\d+\.?\d+)"
    latency = r" +(\d+\.?\d*)% +(\d+\.?\d+)(\w+)"
    detailed_latency = r" +([\d\.]+) +([\d\.]+) +[\d\.]+ +[\d\.inf]+\n"


class UnitMultiplier(Enum):
    s = 1
    ms = 1e-3
    us = 1e-6
    ns = 1e-9


class Parser:
    def parse_stdin(self) -> Tuple[Dict[float, Dict[float, float]], str]:
        wrk_ouput = self.read_stdin()
        parsed_wrk_output = self.parse_wrk_output(wrk_ouput)
        return parsed_wrk_output

    def read_stdin(self) -> str:
        return sys.stdin.read()

    def parse_wrk_output(self, wrk_output: str) -> Tuple[Dict[float, Dict[float, float]], str]:
        parsed = {}  # type: Dict[float, Dict[float, float]]
        website = re.search(RegexLibrary.website.value, wrk_output).group(1)
        req_s = float(re.search(RegexLibrary.req_s.value, wrk_output).group(1))
        parsed[req_s] = {}
        # parse latency
        for matches in re.findall(RegexLibrary.latency.value, wrk_output):
            percentile, result, unit = matches
            scaled_result = round(float(result) * UnitMultiplier[unit].value, 9)
            parsed[req_s][float(percentile)] = scaled_result
        # parse detailed latency, only in wrk2 output
        for matches in re.findall(RegexLibrary.detailed_latency.value, wrk_output):
            result, percentile = matches
            percentile = float(percentile) * 100
            scaled_result = round(float(result) * UnitMultiplier.ms.value, 9)
            parsed[req_s][percentile] = scaled_result

        return parsed, website
