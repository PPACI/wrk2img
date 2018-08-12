import re
from typing import List, Dict


class Parser:
    def parse_stdin(self) -> Dict[str, float]:
        wrk_ouput = self.read_stdin()
        parsed_wrk_output = self.parse_wrk_output(wrk_ouput)
        return parsed_wrk_output

    def read_stdin(self) -> List[str]:
        raise NotImplementedError

    def parse_wrk_output(self, wrk_output: List[str]) -> Dict[str, float]:
        parsed = {}  # type: Dict[str, float]
        multiplier_per_unit = {
            "s": 1,
            "ms": 1e-3,
            "us": 1e-6,
            "ns": 1e-9,
            "MB": 1e6
        }
        for line in wrk_output:
            latency = re.match(" +(\d{2})% (\d+\.?\d+)(\w+)", line)
            if latency is not None:
                percentile, result, unit = latency.groups()
                parsed[percentile] = float(result) * multiplier_per_unit[unit]
            requests = re.match(" *Requests/sec: +(\d+\.?\d+)", line)
            if requests is not None:
                result = requests.groups()[0]
                parsed["req/s"] = float(result)
            transfer = re.match(" *Transfer/sec: +(\d+\.?\d+)(\w+)", line)
            if transfer is not None:
                result, unit = transfer.groups()
                parsed["trans/s"] = float(result) * multiplier_per_unit[unit]
        return parsed
