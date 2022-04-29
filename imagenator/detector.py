import json
import logging
import subprocess
from dataclasses import dataclass


class GrypeException(BaseException):
    """Exception while calling syft CLI"""

    pass


class InvalidSBOMException(BaseException):
    """Exception while invalid SBOM revieved"""

    pass


@dataclass
class Vulnerability:
    name: str
    link: str
    type: str
    package: str
    version: str
    severity: str
    description: str


DEFAULT = "No Data"


def parse(result: dict) -> list[Vulnerability]:
    """Parse JSON output from Grype"""
    if not result:
        return list()

    res: list[Vulnerability] = list()
    for v in result.get("matches", {}):
        severity = v.get("vulnerability", {}).get("severity", "")
        if severity == "High" or severity == "Critical":
            res.append(
                Vulnerability(
                    severity=severity,
                    name=v.get("vulnerability", {}).get("id", DEFAULT),
                    description=v.get("vulnerability", {}).get("description", DEFAULT),
                    link=v.get("vulnerability", {}).get("dataSource", DEFAULT),
                    package=v.get("artifact", {}).get("name", DEFAULT),
                    version=v.get("artifact", {}).get("version", DEFAULT),
                    type=v.get("artifact", {}).get("type", DEFAULT),
                )
            )
    return res


class Detector:
    def check(self, sbom: bytes) -> list[Vulnerability]:
        """Call Grype for permorme vulnerability check"""
        if not sbom:
            raise InvalidSBOMException

        logging.info("Start scanning SBOM")

        out: subprocess.CompletedProcess
        try:
            out = subprocess.run(
                ["grype", "-o", "json"], input=sbom, check=True, capture_output=True
            )
        except subprocess.CalledProcessError as err:
            logging.error(err.stderr)
            raise GrypeException
        return parse(result=json.loads(out.stdout))
