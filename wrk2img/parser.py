import re
import sys
from enum import Enum
from typing import Dict, Tuple


class RegexLibrary(Enum):
    website = r"Running \d+. test @ https?://(.+?)[/\n]"
    req_s = r" *Requests/sec: +(\d+\.?\d*)"
    latency = r" +(\d+\.?\d*)% +(\d+\.?\d*)(\w+)"
    detailed_latency = r" +([\d\.]+) +([\d\.]+) +[\d\.]+ +[\d\.inf]+\n"
    split = r"Running \d+. test .+?Transfer\/sec: +\d+\.?\d*\w+"
    split_after_transfer = r" *Transfer\/sec: +\d+\.?\d*\w+(\n)"


class UnitMultiplier(Enum):
    s = 1
    ms = 1e-3
    us = 1e-6
    ns = 1e-9


class Parser:
    def parse_stdin(self, curve_names: list = None) -> Tuple[Dict[str, Dict[float, float]], str]:
        wrk_ouput = self.read_stdin()
        parsed_wrk_output = self.parse_wrk_output(wrk_ouput, curve_names=curve_names)
        return parsed_wrk_output

    def read_stdin(self) -> str:
        std = []
        for line in sys.stdin:
            print(line.rstrip())
            std.append(line)
        std_concat = "".join(std)
        return std_concat

    def parse_wrk_output(self, wrk_output: str, curve_names: list = None) -> Tuple[Dict[str, Dict[float, float]], str]:
        parsed = {}  # type: Dict[str, Dict[float, float]]
        websites = []
        all_wrk_output = re.findall(RegexLibrary.split.value, wrk_output, flags=re.DOTALL)
        for i, single_wrk_output in enumerate(all_wrk_output):
            websites.append(re.search(RegexLibrary.website.value, single_wrk_output).group(1))
            req_s = float(re.search(RegexLibrary.req_s.value, single_wrk_output).group(1))
            if curve_names is not None and i < len(curve_names):
                label = curve_names[i]
            else:
                label = "{} req/s".format(req_s)
            parsed[label] = {}
            # parse latency
            for matches in re.findall(RegexLibrary.latency.value, single_wrk_output):
                percentile, result, unit = matches
                scaled_result = round(float(result) * UnitMultiplier[unit].value, 9)
                parsed[label][float(percentile)] = scaled_result
            # parse detailed latency, only in wrk2 output
            for matches in re.findall(RegexLibrary.detailed_latency.value, single_wrk_output):
                result, percentile = matches
                percentile = float(percentile) * 100
                scaled_result = round(float(result) * UnitMultiplier.ms.value, 9)
                parsed[label][percentile] = scaled_result
        if len(set(websites)) == 0:
            raise ValueError("No website detected")
        if len(set(websites)) > 1:
            raise ValueError("Multiple different website detected in log")
        else:
            website = websites[0]

        return parsed, website
