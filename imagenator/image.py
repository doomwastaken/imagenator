import logging
import subprocess


class SyftException(BaseException):
    """Exception while calling syft CLI"""

    pass


class Image:
    def decompose(self, container_name: str) -> bytes:
        """Generate SBOM of OCI image in JSON format"""
        if not container_name:
            return bytes()

        logging.info(f"Start generating sbom for image {container_name}")

        out: subprocess.CompletedProcess
        try:
            out = subprocess.run(
                ["syft", f"registry:{container_name}", "-o", "json"],
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as err:
            logging.error(err.stderr)
            raise SyftException

        logging.info("SBOM was generated succefully")

        return out.stdout
